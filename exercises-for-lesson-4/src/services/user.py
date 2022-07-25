from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session, or_

from src.db import AbstractCache, get_session, get_cache
from src.models import User
from src.services import ServiceMixin
from src.utils import get_jwt_payload

__all__ = (
    "UserService",
    "get_user_service"
)


class UserService(ServiceMixin):
    def get_user(self, credentials: str) -> Optional[User]:
        """Вернуть данные пользователя."""
        payload: dict = get_jwt_payload(credentials, options={"verify_signature": False})
        user: User = self.session.query(User).filter(User.uuid == payload["user_uuid"]).first()
        return user.dict() if user else None


# get_user_service — это провайдер UserService. Синглтон
@lru_cache()
def get_user_service(
    session: Session = Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
) -> UserService:
    return UserService(session=session, cache=cache)
