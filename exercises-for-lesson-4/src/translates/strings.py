__all__ = (
    "get_translate",
)


def get_translate(space, key):
    key = str(key)

    if space not in strings:
        return 'unknown space'
    
    if key not in strings[space]:
        return 'unknown key'
    
    return strings[space][key]


strings: dict[str, dict[str, str]] = {
    "create_user_error": {
        "0": "User is exist",
        "1": "User with this email is already exist",
        "2": "User with this username is already exist"
    }
}
