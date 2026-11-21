from abc import ABC, abstractmethod
from ..core.dice import Dice
from .damage import Damage


class DamageHandler(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def handle(self, damage: Damage) -> Damage:
        self.apply(damage)
        if self._next and damage.amount > 0 and not damage.evaded:
            self._next.handle(damage)
        return damage

    @abstractmethod
    def apply(self, damage: Damage) -> None:
        pass


class EvasionHandler(DamageHandler):
    def __init__(self, chance: float):
        super().__init__()
        self.chance = chance

    def apply(self, damage: Damage) -> None:
        if Dice().chance(self.chance):
            damage.evade()


class ArmorHandler(DamageHandler):
    def __init__(self, reduction: float):
        super().__init__()
        self.reduction = reduction

    def apply(self, damage: Damage) -> None:
        damage.reduce_to(round(damage.amount * (1 - self.reduction)))


class BarrierHandler(DamageHandler):
    def __init__(self, points: int):
        super().__init__()
        self.points = points

    def apply(self, damage: Damage) -> None:
        damage.absorb(self.points)
