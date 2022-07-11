from typing import Any, Generator


class CyclicIterator:
    def __init__(self, generator):
        self.__generator = generator
        self.__iterator = iter(generator)

    def __iter__(self) -> Generator[Any, None, None]:
        return self

    def __next__(self):
        next_value: Any

        try:
            next_value = next(self.__iterator)
        except StopIteration:
            self.__iterator = iter(self.__generator)
            next_value = next(self.__iterator)

        return next_value
