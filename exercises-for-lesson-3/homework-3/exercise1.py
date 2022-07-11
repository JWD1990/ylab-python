def cache_decorator(func) -> callable:
    cache: dict[any: any] = {}

    def wrapper(*args, **kwargs) -> any:
        param: any = args[0]

        if param in cache:
            return cache[args[0]]

        return cache.setdefault(param, func(*args, **kwargs))

    return wrapper


if __name__ == '__main__':
    @cache_decorator
    def multiplier(number: int) -> int:
        return number * 2
