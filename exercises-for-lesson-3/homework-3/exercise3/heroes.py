from antagonistfinder import AntagonistFinder
from attacks import FireAGun, Kick, UltimateAttackIncinerateWithLasers


class SuperHero(FireAGun):
    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)

    # Решённая проблема: У разных супергероев разные суперспособности
    # Решение: Применён принцип открытости/закрытости
    # Доп инфа: Метод вызывает суперспособность героя
    # Решённые трудности: Нужные методы добавяться классами-миксинами как и атаки
    def ultimate(self):
        if self.can_use_ultimate_attack:
            self.ultimate_attack()


class Superman(UltimateAttackIncinerateWithLasers, Kick, SuperHero):
    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)
