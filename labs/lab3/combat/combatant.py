from abc import ABC, abstractmethod
from .hit import Hit
from ..defense.damage import Damage


class Combatant(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @abstractmethod
    def roll_damage(self) -> Hit: ...

    @abstractmethod
    def receive_hit(self, amount: int) -> Damage: ...

    def is_alive(self) -> bool:
        return self.health > 0
