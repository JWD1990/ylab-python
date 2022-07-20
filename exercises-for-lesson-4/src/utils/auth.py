from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from src.core import config

__all__ = (
    "get_hash_password",
    "verify_password"
)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(password: str) -> str:
    return password_context.hash(password)
