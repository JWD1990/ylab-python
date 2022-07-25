signup_responses: dict = {
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "examples": {
                    "user": {
                        "summary": "Такой пользователь уже есть",
                        "value": {"error_code": 0, "msg": "User is exist"}
                    },
                    "email": {
                        "summary": "Почта занята другим пользователем",
                        "value": {"error_code": 1, "msg": "User with this email is already exist"}
                    },
                    "username": {
                        "summary": "Такое имя пользователя уже занято",
                        "value": {"error_code": 2, "msg": "User with this username is already exist"}
                    },
                }
            }
        }
    }
}