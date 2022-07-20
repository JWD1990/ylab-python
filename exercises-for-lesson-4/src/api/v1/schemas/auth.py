from pydantic import BaseModel

from src.api.v1.schemas.users import UserProfile

__all__ = (
    "SignupResponse",
)


class SignupResponse(BaseModel):
    msg: str = 'User created'
    user: UserProfile
