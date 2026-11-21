from ..enemy.enemies import Enemy, Dragon, HauntedWeapon
from ..enemy.decorators import LegendaryEnemy, WindfuryEnemy, ArmoredEnemy
from ..core.dice import Dice


class Location:
    def __init__(self, name):
        self.name = name

    def create_enemy(self):
        raise NotImplementedError


class Forest(Location):
    def __init__(self):
        super().__init__("Мистический лес")

    def create_enemy(self):
        enemy = Enemy("Гоблин", 50, (8, 14), 40)
        return decorate_enemy(enemy)


class Crypt(Location):
    def __init__(self):
        super().__init__("Склеп")

    def create_enemy(self):
        enemy = Enemy("Скелет", 65, (10, 16), 60)
        return decorate_enemy(enemy)


class DragonLair(Location):
    def __init__(self):
        super().__init__("Логово дракона")

    def create_enemy(self):
        return decorate_enemy(Dragon())


class HauntedManor(Location):
    def __init__(self):
        super().__init__("Проклятый особняк")

    def create_enemy(self):
        weapon = {"name": "Эльфийский лук", "damage": 14, "price": 90}
        return decorate_enemy(HauntedWeapon(weapon))


def decorate_enemy(enemy):
    dice = Dice()
    if dice.chance(0.35):
        enemy = LegendaryEnemy(enemy)
    if dice.chance(0.30):
        enemy = WindfuryEnemy(enemy)
    if dice.chance(0.30):
        enemy = ArmoredEnemy(enemy)
    return enemy
