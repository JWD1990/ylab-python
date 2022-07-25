from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.api.v1.schemas import UserProfile
from fastapi.security import HTTPAuthorizationCredentials
from src.services import UserService, get_user_service, get_auth_service

router = APIRouter()


@router.get(
    path="/me",
    response_model=UserProfile,
    summary="Просмотр профиля",
    tags=["user_profile"],
    status_code=HTTPStatus.CREATED,
    response_model_exclude={"id", "password", "is_totp_enabled", "is_active"}
)
def get_userprofile(
    credentials: HTTPAuthorizationCredentials = Depends(get_auth_service().get_jwtbearer()),
    user_service: UserService = Depends(get_user_service),
) -> UserProfile:
    data: dict = user_service.get_user(credentials)

    if not data:
        HTTPException(HTTPStatus.BAD_REQUEST, detail="User does't exist")

    return UserProfile(**data)
