from http import HTTPStatus

from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.api.v1.schemas import UserCreate, UserLogin, SignupResponse, LoginResponse, RefreshResponse
from src.services import AuthService, get_auth_service
from src.custom_swagger_docs import signup_responses

router = APIRouter()


@router.post(
    path="/signup",
    response_model=SignupResponse,
    responses=signup_responses,
    summary="Регистрация пользователя",
    tags=["auth"],
    status_code=HTTPStatus.CREATED,
    response_model_exclude_none=True,
    response_model_exclude={"user": {"id", "password"}}
)
def get_signup(
    user_data: UserCreate,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> SignupResponse:
    data: dict = auth_service.create_user(user_data)
    if 'error_code' in data:
        # Пересечение по email и / или username, отдадим 400 и расшифровку ошибки
        response.status_code = HTTPStatus.BAD_REQUEST
        return SignupResponse(**data)
    else:
        return SignupResponse(user=data)


@router.post(
    path="/login",
    response_model=LoginResponse,
    summary="Авторизация пользователя",
    tags=["auth"],
    status_code=HTTPStatus.OK,
)
def get_login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    data: dict = auth_service.login_user(user_data)

    if not data:
        # username - password пара не корректная, отдадим 400
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Username or password incorrect")

    return LoginResponse(**data)


@router.post(
    path="/refresh",
    response_model=RefreshResponse,
    summary="Выдача новой JWT-пары токенов",
    tags=["auth"],
    status_code=HTTPStatus.OK,
)
def get_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(get_auth_service().get_jwtbearer(type_token="refresh")),
    auth_service: AuthService = Depends(get_auth_service),
) -> RefreshResponse:
    data: dict = auth_service.refresh_tokens(credentials)

    if not data:
        # Нет юзера, отдадим 400
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Refresh token is incorrect")

    return RefreshResponse(**data)
