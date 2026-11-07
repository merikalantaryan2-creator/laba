from ..combat.combatant import Combatant
from ..combat.hit import Hit
from ..core.dice import Dice
from ..defense.damage import Damage
from ..defense.handlers import EvasionHandler, ArmorHandler, BarrierHandler


class Hero(Combatant):
    def __init__(self, name, hero_class="Воин"):
        self._name = name
        self.hero_class = hero_class
        self.max_health = 100 if hero_class == "Воин" else 85
        self._health = self.max_health
        self.gold = 50
        self.experience = 0
        self.level = 1
        self.inventory = []
        self.achievements = []
        self.defense = EvasionHandler(0.10)
        self.defense.set_next(ArmorHandler(0.10)).set_next(BarrierHandler(5))

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    def roll_damage(self):
        return Hit(Dice().roll(10, 18), Dice().chance(0.15))

    def receive_hit(self, amount):
        result = self.defense.handle(Damage(amount))
        self._health = max(0, self._health - result.amount)
        return result

    def rest(self):
        self._health = self.max_health

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level += 1
            self.max_health += 15
            self.rest()
