from datetime import datetime
from uuid import uuid4
from typing import Optional

from sqlmodel import JSON, Column, Field, SQLModel
from sqlalchemy.dialects.postgresql import JSON

__all__ = ("User",)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False)
    roles: list[str] = Field(sa_column=Column(JSON), default=[])
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    is_superuser: bool = Field(default=False)
    uuid: str = Field(default=str(uuid4()))
    is_totp_enabled: bool = Field(default=False)
    is_active: bool = Field(default=True)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
