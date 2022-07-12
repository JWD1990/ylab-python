from abc import ABC, abstractmethod
from places import Place
from heroes import SuperHero


class MassMedia(ABC):
    @abstractmethod
    def create_news(self):
        ...


class Newspapers(MassMedia):
    # Решённая проблема: Герой не должен заниматься оповещениями о своей победе, это задача масс-медиа.
    # Решение: Применён принцип единой ответственности.
    # Доп инфа: Добавлен абстрактный класс MassMedia, обязывающий реализовать метод вывода информации,
    # и класс Newspapers (вариант по заданию)
    # Решённые трудности: Теперь нет проблем добавлять источники информации, которые могут оповещать даже планеты,
    # используя координаты, coordinates:List[float]), вместо атрибута name:str

    def create_news(self, hero: SuperHero, place: Place):
        place_name = getattr(place, 'name', 'place')
        hero_name = getattr(hero, 'name', 'place')
        print(f'{hero_name} saved the {place_name}!')
