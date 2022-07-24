import json

from pydantic import BaseModel, validator
from src.models import User

__all__ = (
    "UserCreate",
    "UserLogin",
    "UserProfile",
)


class UserBase(BaseModel):
    email: str


class UserBaseLogin(BaseModel):
    username: str


class UserLogin(UserBaseLogin):
    password: str


class UserCreate(UserLogin, UserBase):
    ...


class UserProfile(User):
    @validator('roles', pre=True)
    def json_decode(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                pass
        return v
