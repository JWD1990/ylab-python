from time import time
from passlib.context import CryptContext
from datetime import datetime
from typing import Literal, Union, Optional
import jwt
from src.core import config
from src.models import User
from src.api.v1.schemas import UserProfile
from uuid import uuid4

__all__ = (
    "get_hash_password",
    "verify_password",
    "create_tokens",
    "get_jwt_payload",
    "create_token",
    "TypeToken"
)


TypeToken = Union[Literal["access"], Literal["refresh"]]
JwtEncodeConfig = dict[
    Union[Literal["token_expiration"], Literal["secret"]],
    int
]


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hash_pass: str) -> bool:
    result: bool = False

    try:
        result = password_context.verify(password, hash_pass)
    except:
        ...
    
    return result


def get_jwt_encode_config(type_token: TypeToken) -> JwtEncodeConfig:
    """Получение настроек для каждого типа токена"""
    data: JwtEncodeConfig = {
        "token_expiration": (config.JWT_ACCESS_TOKEN_EXPIRE_IN_SECONDS if type_token == 'access' else
                    config.JWT_REFRESH_TOKEN_EXPIRE_IN_SECONDS),
        "secret": (config.JWT_SECRET_KEY if type_token == 'access' else
                    config.JWT_REFRESH_SECRET_KEY)
    }

    return data


def make_token_payload(type: str, tokens_data: dict, user_data: UserProfile, token_expiration: int) -> dict:
    """Подготавливает нагрузку каждого токена"""
    current_time: datetime = datetime.utcnow()
    valid_start_time: int = int(current_time.timestamp())
    payload: dict = {
        "fresh": False,
        "user_uuid": user_data.uuid,
        "iat": valid_start_time,
        "nbf": valid_start_time,
        "exp": valid_start_time + token_expiration,
        "type": type,
        "jti": tokens_data[f"uuid_{type}_token"]
    }
    
    if type == "access":
        payload["refresh_uuid"] = tokens_data["uuid_refresh_token"]

        for name_field in ["username", "email", "is_superuser", "roles"]:
            payload[name_field] = getattr(user_data, name_field)
        
        payload["created_at"] = str(getattr(user_data, "created_at"))
    
    return payload


def create_token(payload: dict, encode_config: dict = None) -> str:
    """Создаст и вернёт токен"""
    if not encode_config or encode_config and "secret" not in encode_config:
        encode_config: JwtEncodeConfig = get_jwt_encode_config(payload["type"])

    return jwt.encode(payload, encode_config["secret"], config.JWT_ALGORITHM)


def create_tokens(db_user_data: User, refresh_token_uuid: str = None) -> dict:
    """Даст созданные токены и немного инфы из них"""
    user_data: UserProfile = UserProfile(**db_user_data.dict())
    tokens_types: list[TypeToken] = ["refresh", "access"]
    tokens_data: dict = {
        "uuid_refresh_token": str(uuid4()) if not refresh_token_uuid else refresh_token_uuid,
        "uuid_access_token": str(uuid4()),
        "tokens": {}
    }

    for type in tokens_types:
        if refresh_token_uuid and type == 'refresh':
            continue

        encode_config: JwtEncodeConfig = get_jwt_encode_config(type)
        payload: dict = make_token_payload(
            type,
            tokens_data,
            user_data,
            encode_config["token_expiration"]
        )
        tokens_data["tokens"][f'{type}_token'] = create_token(payload, encode_config)

    return tokens_data


def get_jwt_payload(token: str, type_token: TypeToken = "access", options: dict = {}) -> dict:
    """Вернёт payload, если всё ок"""
    encode_config: dict = get_jwt_encode_config(type_token)
    payload: Optional[dict] = None

    try:
        payload: dict = jwt.decode(
            token.encode(),
            encode_config["secret"],
            algorithms=[config.JWT_ALGORITHM],
            options=options
        )
    except:
        payload["error"] = "Some error with JWT-token"
    
    return payload
