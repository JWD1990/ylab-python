from typing import Optional
from pydantic import BaseModel

from src.api.v1.schemas import UserProfile

__all__ = (
    "SignupResponse",
    "LoginResponse",
    "TokensRefreshResponse"
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


class SignupBaseResponse(BaseModel):
    msg: str = 'User created'


class BadSignupResponse(SignupBaseResponse):
    error_code: Optional[int]


class SuccessSignup(SignupBaseResponse):
    user: Optional[UserProfile]


class SignupResponse(BadSignupResponse, SuccessSignup):
    ...

    class Config:
        schema_extra = {
            "example": {
                "msg": "User created",
                "user": user_data
            }
        }


class BadLoginResponse(BaseModel):
    msg: Optional[str]
    error_code: Optional[int]


class SuccessLoginResponse(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]


class LoginResponse(BadLoginResponse, SuccessLoginResponse):
    ...

    class Config:
        schema_extra = {
            "example": {
                "access_token": "str",
                "refresh_token": "str"
            }
        }


class TokensRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
