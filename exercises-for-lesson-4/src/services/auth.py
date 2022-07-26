from functools import lru_cache

from http import HTTPStatus
from fastapi import Depends
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, or_

from src.api.v1.schemas import UserCreate, UserLogin
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin
from src.utils import (
    get_hash_password,
    verify_password,
    create_tokens,
    get_jwt_payload,
    check_user_data_intersection,
    TypeToken
)
from src.status_codes import UserErrorsCodes
from src.utils.error_status import get_error_response_data

__all__ = (
    "AuthService",
    "get_auth_service",
)


class JWTBearer(HTTPBearer):
    """Класс для валидации авторизации"""
    def __init__(self, type_token: TypeToken, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.type_token = type_token

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authorization code.")

        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid authentication scheme.")

        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Invalid token or expired token.")

        return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        if "error" in get_jwt_payload(jwtoken, self.type_token):
            return False
        
        return True


class AuthService(ServiceMixin):
    def create_user(self, user_data: UserCreate) -> dict:
        """Создать пользователя."""
        user: User = self.session.query(User).filter(
            or_(User.username == user_data.username, User.email == user_data.email)
        ).first()

        if user:
            return check_user_data_intersection(user, user_data)

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=get_hash_password(user_data.password)
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()

    def login_user(self, user_data: UserLogin) -> dict:
        """Выдать JWT-пару, если пройдена идентификация и аутентификация"""
        user: User = self.session.query(User).filter(User.username == user_data.username).first()

        if not user or user and not verify_password(user_data.password, user.password):
            return get_error_response_data(UserErrorsCodes.USERNAME_EMAIL_PAIR_DOES_NOT_EXIST)

        return create_tokens(user)["tokens"]
    
    def refresh_tokens(self, credentials: str) -> dict:
        """Выдать новую JWT-пару, если есть пользователь"""
        payload: dict = get_jwt_payload(credentials, type_token="refresh", options={"verify_signature": False})
        user: User = self.session.query(User).filter(User.uuid == payload["user_uuid"]).first()
        return create_tokens(user)["tokens"] if user else None

    def get_jwtbearer(self, type_token: TypeToken = "access"):
        return JWTBearer(type_token=type_token)


# get_auth_service — это провайдер AuthService. Синглтон
@lru_cache()
def get_auth_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),
) -> AuthService:
    return AuthService(cache=cache, session=session)
