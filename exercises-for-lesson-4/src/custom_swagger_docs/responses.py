from src.api.v1.schemas import BadResponseBase
from src.status_codes import UserErrorsCodes
from src.utils import get_error_response_data

__all__=(
    "intersection_responses",
    "user_not_found_response",
    "bad_update_userprofile_response",
    "bad_authorisation_data_response",
)


intersection_responses: dict = {
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "examples": {
                    "user": {
                        "summary": "Такой пользователь уже есть",
                        "value": get_error_response_data(UserErrorsCodes.USER_IS_EXITS)
                    },
                    "email": {
                        "summary": "Почта занята другим пользователем",
                        "value": get_error_response_data(UserErrorsCodes.EMAIL_INTERSECTION)
                    },
                    "username": {
                        "summary": "Такое имя пользователя уже занято",
                        "value": get_error_response_data(UserErrorsCodes.USERNAME_INTERSECTION)
                    },
                }
            }
        }
    }
}

user_not_found_response: dict = {
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "examples": {
                    "not_user": {
                        "summary": "Такой пользователь не существует",
                        "value": get_error_response_data(UserErrorsCodes.USER_DOES_NOT_EXIST)
                    }
                }
            }
        }
    }
}

bad_update_userprofile_response: dict = {**intersection_responses, **user_not_found_response}

bad_authorisation_response_data: BadResponseBase = get_error_response_data(UserErrorsCodes.USERNAME_EMAIL_PAIR_DOES_NOT_EXIST)
bad_authorisation_data_response: dict = {
    400: {
        "description": bad_authorisation_response_data["msg"],
        "content": {
            "application/json": {
                "examples": {
                    "not_user": {
                        "summary": "Такой пользователь не существует",
                        "value": bad_authorisation_response_data
                    }
                }
            }
        }
    }
}
