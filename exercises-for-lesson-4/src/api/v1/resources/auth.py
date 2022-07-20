from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.schemas import UserCreate, SignupResponse
from src.services import AuthService, get_auth_service

router = APIRouter()


@router.post(
    path="/",
    response_model=SignupResponse,
    summary="Регистрация пользователя",
    tags=["signup"],
    status_code=HTTPStatus.CREATED,
)
def get_signup(
    user_data: UserCreate,
    user_service: AuthService = Depends(get_auth_service),
) -> SignupResponse:
    data: dict = user_service.create_user(user_data)

    if not data:
        # Пересечение по email и / или username, отдадим 400
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email or / and usermname is already exist")

    return SignupResponse(user=data)
