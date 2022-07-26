import json
from typing import Optional

from pydantic import BaseModel, validator
from src.models import User
from src.translates import get_translate

__all__ = (
    "UserCreate",
    "UserLogin",
    "UserProfile",
    "UserProfileResponse",
    "UserProfileUpdateData",
    "UserProfileUpdateResponse",
)


userprofile_data = {
    "username": "cmd",
    "roles": [],
    "created_at": "2022-07-25T23:11:07.569894",
    "is_superuser": False,
    "uuid": "ca0ffcc4-5f6b-48a8-a49f-03f4dbfc93df",
    "email": "cmd@mail.ru"
}

user_data: dict = {
    **userprofile_data,
    "is_totp_enabled": False,
    "is_active": True,
}


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


class BaseUserProfileResponse(BaseModel):
    msg: str = 'User created'


class BadUserProfileResponse(BaseUserProfileResponse):
    error_code: Optional[int]


class SuccessUserProfileResponse(BaseUserProfileResponse):
    user: Optional[UserProfile]


class UserProfileResponse(BadUserProfileResponse, SuccessUserProfileResponse):
    ...

    class Config:
        schema_extra = {
            "example": {
                "user": userprofile_data
            }
        }


class UserProfileUpdateData(BaseModel):
    username: Optional[str] = None
    is_totp_enabled: Optional[bool] = None
    email: Optional[str] = None
    password: Optional[str] = None


class SuccessUserProfileResponse(BaseUserProfileResponse):
    user: Optional[UserProfile]



class BaseUserProfileUpdateResponse(BaseModel):
    msg: str = get_translate("user_data", "success_update")


class BadUpdateUserProfileResponse(BaseUserProfileUpdateResponse):
    error_code: Optional[int]


class SuccessUserProfileUpdateResponse(BaseUserProfileUpdateResponse):
    user: Optional[UserProfile]
    access_token: Optional[str]


class UserProfileUpdateResponse(BadUpdateUserProfileResponse, SuccessUserProfileUpdateResponse):
    ...

    class Config:
        schema_extra = {
            "example": {
                "msg": get_translate("user_data", "success_update"),
                "user": user_data,
                "access_token": "str"
            }
        }
