from typing import Optional
from pydantic import BaseModel

from src.api.v1.schemas.users import UserProfile

__all__ = (
    "SignupResponse",
    "LoginResponse",
    "RefreshResponse"
)


class SignupBaseResponse(BaseModel):
    msg: str = 'User created'


class BadSignup(SignupBaseResponse):
    error_code: Optional[int]


class SuccessSignup(SignupBaseResponse):
    user: Optional[UserProfile]


class SignupResponse(BadSignup, SuccessSignup):
    ...


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshResponse(LoginResponse):
    ...
