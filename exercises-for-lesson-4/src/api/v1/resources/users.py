from http import HTTPStatus

from fastapi import APIRouter, Depends, Response
from src.api.v1.schemas import UserProfileResponse, UserProfileUpdateData, UserProfileUpdateResponse
from fastapi.security import HTTPAuthorizationCredentials
from src.services import UserService, get_user_service, get_auth_service
from src.custom_swagger_docs import user_not_found_response, bad_update_userprofile_response

router = APIRouter()


@router.get(
    path="/me",
    response_model=UserProfileResponse,
    responses=user_not_found_response,
    summary="Просмотр профиля",
    tags=["user_profile"],
    status_code=HTTPStatus.OK,
    response_model_exclude_none=True,
    response_model_exclude={"user" :{"id", "password", "is_totp_enabled", "is_active"}}
)
def get_userprofile(
    response: Response,
    credentials: HTTPAuthorizationCredentials = Depends(get_auth_service().get_jwtbearer()),
    user_service: UserService = Depends(get_user_service),
) -> UserProfileResponse:
    data: dict = user_service.get_user(credentials)

    if "error_code" in data:
        response.status_code = HTTPStatus.NOT_FOUND
        return UserProfileResponse(**data)
    else:
        return UserProfileResponse(user=data)


@router.patch(
    path="/me",
    response_model=UserProfileUpdateResponse,
    responses=bad_update_userprofile_response,
    summary="Редактирование профиля",
    tags=["user_profile"],
    status_code=HTTPStatus.OK,
    response_model_exclude_none=True,
    response_model_exclude={"user": {"id", "password"}}
)
def get_userprofile(
    user_data: UserProfileUpdateData,
    response: Response,
    credentials: HTTPAuthorizationCredentials = Depends(get_auth_service().get_jwtbearer()),
    user_service: UserService = Depends(get_user_service),
) -> UserProfileUpdateResponse:
    data: dict = user_service.update_user(credentials, user_data)

    if "error" in data:
        response.status_code = HTTPStatus.BAD_REQUEST

    return UserProfileUpdateResponse(**data)
