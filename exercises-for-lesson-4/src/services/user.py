from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session, and_, or_
from src.api.v1.schemas import UserProfileUpdateData

from src.db import AbstractCache, get_session, get_cache
from src.models import User
from src.services import ServiceMixin
from src.utils import (
    get_jwt_payload,
    create_tokens,
    check_user_data_intersection,
    get_error_response_data,
    get_hash_password
)
from src.status_codes import UserErrorsCodes

__all__ = (
    "UserService",
    "get_user_service"
)


class UserService(ServiceMixin):
    def get_user(self, credentials: str) -> dict:
        """Вернуть данные пользователя."""
        payload: dict = get_jwt_payload(credentials, options={"verify_signature": False})
        user: User = self.session.query(User).filter(User.uuid == payload["user_uuid"]).first()
        return user.dict() if user else get_error_response_data(UserErrorsCodes.USER_DOES_NOT_EXIST)
    
    def update_user(self, credentials: str, user_data: UserProfileUpdateData) -> dict:
        payload: dict = get_jwt_payload(credentials, options={"verify_signature": False})
        user: User = self.session.query(User).filter(User.uuid == payload["user_uuid"]).first()

        if not user:
            return get_error_response_data(UserErrorsCodes.USER_DOES_NOT_EXIST)

        other_user: User = self.session.query(User).filter(
            and_(
                or_(
                    User.email == user_data.email,
                    User.username == user_data.username,
                ),
                User.uuid != payload["user_uuid"]
            )
        ).first()

        if other_user:
            return check_user_data_intersection(other_user, user_data)

        update_data = user_data.dict(exclude_unset=True)

        for key, value in update_data.items():
            if key == "password":
                value = get_hash_password(value)

            setattr(user, key, value)
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return {
            "user": user.dict(),
            "access_token": create_tokens(user, payload["refresh_uuid"])["tokens"]["access_token"]
        }


# get_user_service — это провайдер UserService. Синглтон
@lru_cache()
def get_user_service(
    session: Session = Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
) -> UserService:
    return UserService(session=session, cache=cache)
