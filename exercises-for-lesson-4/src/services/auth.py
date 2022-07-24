from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session, or_

from src.api.v1.schemas import UserCreate, UserLogin
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin
from src.utils import get_hash_password, verify_password, create_tokens
from src.translates import get_translate

__all__ = ("AuthService", "get_auth_service")


class AuthService(ServiceMixin):
    def create_user(self, user_data: UserCreate) -> dict:
        """Создать пользователя."""
        user: User = self.session.query(User).filter(
            or_(User.username == user_data.username, User.email == user_data.email)
        ).first()

        if user:
            number_error: int

            # чтобы на клиенте можно было сделать красивый и с явным указанием на ошибку интерфейс
            if user.email == user_data.email and user.username == user_data.username:
                number_error = 0
            elif user.email == user_data.email:
                number_error = 1
            elif user.username == user_data.username:
                number_error = 2
            
            return {
                "error_code": number_error,
                "msg": get_translate("create_user_error", number_error)
            }

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
        user = self.session.query(User).filter(User.username == user_data.username).first()

        if (not user or 
            user and not verify_password(password=user_data.password, hash_pass=user.password)):
            return None
        
        tokens_data: any = create_tokens(user)

        return tokens_data["tokens"]


# get_user_service — это провайдер UserService. Синглтон
@lru_cache()
def get_auth_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),

) -> AuthService:
    return AuthService(cache=cache, session=session)
