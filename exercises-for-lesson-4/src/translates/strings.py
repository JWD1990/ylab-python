from src.status_codes import UserErrorsCodes

__all__ = (
    "get_translate",
)


def get_translate(space, key):
    if space not in strings:
        return 'unknown space'
    
    if key not in strings[space]:
        return 'unknown key'
    
    return strings[space][key]


strings: dict[str, dict[str, str]] = {
    "user_error": {
        UserErrorsCodes.USER_DOES_NOT_EXIST: "User does't exist",
        UserErrorsCodes.USER_IS_EXITS: "User is exist",
        UserErrorsCodes.EMAIL_INTERSECTION: "User with this email is already exist",
        UserErrorsCodes.USERNAME_INTERSECTION: "User with this username is already exist",
        UserErrorsCodes.USERNAME_EMAIL_PAIR_DOES_NOT_EXIST: "Username password pair does't exist"
    },
    "user_data": {
        "success_update": "Update is successful. Please use new access_token."
    }
}
