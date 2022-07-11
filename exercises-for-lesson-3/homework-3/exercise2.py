import time


def factor_decorator(call_count: int, start_sleep_time: float, factor: float, border_sleep_time: float):
    def decorator(func) -> callable:
        def wrapper(*args, **kwargs) -> callable:
            nonlocal start_sleep_time

            attempt: int = 1
            result: bool

            print(f'Кол-во запусков = {call_count}', 'Начало работы', sep='\n')

            while attempt <= call_count:
                print(f'Запуск номер {attempt}. Ожидание: {start_sleep_time} секунд.', end=' ', flush=True)
                time.sleep(start_sleep_time)
                result = func(*args, **kwargs)
                print(f'Результат декорируемой функций = {result}.', flush=True)
                attempt += 1

                if start_sleep_time < border_sleep_time:
                    start_sleep_time *= 2 ** factor

                # время после увеличения могло стать больше border_sleep_time
                if start_sleep_time > border_sleep_time:
                    start_sleep_time = (start_sleep_time if start_sleep_time < border_sleep_time
                                        else border_sleep_time)

            print('Конец работы')

        return wrapper

    return decorator


@factor_decorator(5, 1, 2, 15)
def my_func() -> bool:
    return False


if __name__ == '__main__':
    my_func()
