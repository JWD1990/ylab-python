from datetime import datetime
import json

from pydantic import BaseModel, validator

__all__ = (
    "UserCreate",
    "UserProfile"
)

class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class UserProfile(UserBase):
    roles: list[str] = []
    created_at: datetime
    is_superuser: bool
    uuid: str
    is_totp_enabled: bool
    is_active: bool

    class Config:
        exclude = {"id", "password"}

    @validator('roles', pre=True)
    def json_decode(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except ValueError:
                pass
        return v
