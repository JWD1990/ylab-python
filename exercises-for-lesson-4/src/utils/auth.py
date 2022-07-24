from time import time
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Literal, Union
import jwt
from src.core import config
from src.models import User
from src.api.v1.schemas.users import UserProfile
from uuid import uuid4

__all__ = (
    "get_hash_password",
    "verify_password",
    "create_tokens",
    "get_payload"
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
    return password_context.verify(password, hash_pass)


def get_jwt_encode_config(type_token: TypeToken) -> JwtEncodeConfig:
    """Получение настроек для каждого типа токена"""
    data: JwtEncodeConfig = {
        "token_expiration": (config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES if type_token == 'access' else
                    config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES),
        "secret": (config.JWT_SECRET_KEY if type_token == 'access' else
                    config.JWT_REFRESH_SECRET_KEY)
    }

    return data


def make_token_payload(type: str, tokens_data: dict, user_data: UserProfile, token_expiration: int) -> dict:
    """Подготавливает нагрузку каждого токена"""
    valid_start_time: datetime = datetime.utcnow()
    payload: dict = {
        "fresh": False,
        "user_uuid": user_data.uuid,
        "iat": int(valid_start_time.timestamp()),
        "nbf": int(valid_start_time.timestamp())
    }

    token_expiration: datetime = valid_start_time + timedelta(minutes=token_expiration)

    payload["exp"] = int(token_expiration.timestamp())
    payload["type"] = type
    payload["jti"] = tokens_data[f"uuid_{type}_token"]
    
    if type == "access":
        payload["refresh_uuid"] = tokens_data["uuid_refresh_token"]

        for name_field in ["username", "email", "is_superuser", "roles"]:
            payload[name_field] = getattr(user_data, name_field)
        
        payload["created_at"] = str(getattr(user_data, "created_at"))
    
    return payload


def create_tokens(db_user_data: User) -> dict:
    """Даст созданные токены и немного инфы из них"""
    user_data: UserProfile = UserProfile(**db_user_data.dict())
    tokens_types: list[TypeToken] = ["refresh", "access"]
    tokens_data: dict = {
        "uuid_refresh_token": str(uuid4()),
        "uuid_access_token": str(uuid4()),
        "tokens": {}
    }

    for type in tokens_types:
        encode_config: JwtEncodeConfig = get_jwt_encode_config(type)
        payload: dict[str, any] = make_token_payload(
            type,
            tokens_data,
            user_data,
            encode_config["token_expiration"]
        )
        tokens_data["tokens"][f'{type}_token'] = jwt.encode(payload, encode_config["secret"], config.JWT_ALGORITHM)

    return tokens_data
