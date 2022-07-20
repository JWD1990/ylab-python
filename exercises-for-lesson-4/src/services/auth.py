from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session, or_

from src.api.v1.schemas import UserCreate
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin
from src.utils import get_hash_password

__all__ = ("AuthService", "get_auth_service")


class AuthService(ServiceMixin):
    def create_user(self, user_data: UserCreate) -> dict:
        """Создать пользователя."""
        user = self.session.query(User).filter(
            or_(User.username == user_data.username, User.email == user_data.email)
        ).first()

        if user:
            return None

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=get_hash_password(user_data.password)
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()


# get_user_service — это провайдер UserService. Синглтон
@lru_cache()
def get_auth_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),

) -> AuthService:
    return AuthService(cache=cache, session=session)
