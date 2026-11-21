from ..combat.combatant import Combatant
from ..combat.hit import Hit
from ..core.dice import Dice
from ..defense.damage import Damage


class Enemy(Combatant):
    def __init__(self, name="Гоблин", health=50, damage=(8, 14), reward=40):
        self._name = name
        self._health = health
        self.max_health = health
        self.damage_range = damage
        self.experience_reward = reward

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    def roll_damage(self):
        return Hit(Dice().roll(*self.damage_range))

    def receive_hit(self, amount):
        result = Damage(max(0, amount))
        self._health = max(0, self._health - result.amount)
        return result


class Dragon(Enemy):
    def __init__(self):
        super().__init__("Дракон", 150, (15, 25), 300)


class HauntedWeapon(Enemy):
    # адаптер: превращает оружие в объект с интерфейсом врага
    def __init__(self, weapon):
        self.weapon = weapon
        super().__init__(f"Одержимый {weapon['name']}", weapon['damage'] * 5,
                         (weapon['damage'] - 2, weapon['damage'] + 2), weapon['price'] // 2)
