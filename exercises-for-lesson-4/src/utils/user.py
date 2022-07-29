from src.api.v1.schemas import UserProfileUpdateData

from src.models import User
from src.status_codes import UserErrorsCodes
from src.utils.error_status import get_error_response_data

__all__ = (
    "check_user_data_intersection",
)


def check_user_data_intersection(db_user: User, user_data: UserProfileUpdateData) -> dict:
    """
        Вернёт расшифровку по коллизиям с другими пользователями,
        чтобы на клиенте можно было сделать красивый и с явным указанием на ошибку интерфейс
    """
    if db_user.email == user_data.email and db_user.username == user_data.username:
        return get_error_response_data(UserErrorsCodes.USER_IS_EXITS)
    elif db_user.email == user_data.email:
        return get_error_response_data(UserErrorsCodes.EMAIL_INTERSECTION)
    elif db_user.username == user_data.username:
        return get_error_response_data(UserErrorsCodes.USERNAME_INTERSECTION)
