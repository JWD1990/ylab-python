import time


def factor_decorator(call_count: int, start_sleep_time: float, factor: float, border_sleep_time: float) -> callable:
    def decorator(func) -> callable:
        def wrapper(*args, **kwargs) -> callable:
            sleep_time: float = start_sleep_time

            print(f'Кол-во запусков = {call_count}', 'Начало работы', sep='\n')

            for call in range(0, call_count):
                if sleep_time < border_sleep_time:
                    sleep_time = start_sleep_time * factor ** call

                # время после увеличения могло стать больше border_sleep_time
                if sleep_time > border_sleep_time:
                    sleep_time = border_sleep_time

                print(f'Запуск номер {call + 1}. Ожидание: {sleep_time} секунд.', end=' ', flush=True)
                time.sleep(sleep_time)
                result: any = func(*args, **kwargs)
                print(f'Результат декорируемой функций = {result}.')

            print('Конец работы')

        return wrapper

    return decorator
