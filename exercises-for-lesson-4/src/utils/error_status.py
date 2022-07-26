from src.translates import get_translate
from src.api.v1.schemas import BadResponseBase

__all__=(
    "get_error_response_data",
)


def get_error_response_data(error_code: int) -> BadResponseBase:
    return {
        "error_code": error_code,
        "msg": get_translate("user_error", error_code)
    }
