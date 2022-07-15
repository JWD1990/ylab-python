def cache_decorator(func) -> callable:
    cache: dict[any: any] = {}

    def wrapper(*args, **kwargs) -> any:
        param: any = args[0]

        if param not in cache:
            cache[param] = func(*args, **kwargs)

        return cache[param]

    return wrapper


@cache_decorator
def multiplier(number: int) -> int:
    return number * 2
