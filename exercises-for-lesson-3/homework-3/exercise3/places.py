from abc import ABC, abstractmethod


class Place(ABC):
    @abstractmethod
    def get_antogonist(self):
        ...


class Kostroma(Place):
    city_name = 'Kostroma'

    def get_antogonist(self):
        print('Orcs hid in the forest')


class Tokyo(Place):
    name = 'Tokyo'

    def get_antogonist(self):
        print('Godzilla stands near a skyscraper')
