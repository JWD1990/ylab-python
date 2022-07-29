from typing import Optional
from pydantic import BaseModel

__all__=(
    "BaseResponseWithMsg",
    "BadResponseBase",
)


class BaseResponseWithMsg(BaseModel):
    msg: str


class BadResponseBase(BaseResponseWithMsg):
    error_code: Optional[int]
