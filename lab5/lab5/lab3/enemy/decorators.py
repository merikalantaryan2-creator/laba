from ..defense.damage import Damage
from ..combat.hit import Hit


class EnemyDecorator:
    # базовый декоратор делегирует вызовы исходному врагу
    def __init__(self, enemy):
        self.enemy = enemy

    @property
    def name(self):
        return self.enemy.name

    @property
    def health(self):
        return self.enemy.health

    @property
    def max_health(self):
        return self.enemy.max_health

    @property
    def experience_reward(self):
        return self.enemy.experience_reward

    def is_alive(self):
        return self.enemy.is_alive()

    def roll_damage(self):
        return self.enemy.roll_damage()

    def receive_hit(self, amount):
        return self.enemy.receive_hit(amount)


class LegendaryEnemy(EnemyDecorator):
    @property
    def name(self):
        return "Легендарный " + self.enemy.name

    @property
    def experience_reward(self):
        return self.enemy.experience_reward * 2

    def roll_damage(self):
        hit = self.enemy.roll_damage()
        return Hit(hit.damage * 2, hit.critical)


class WindfuryEnemy(EnemyDecorator):
    @property
    def name(self):
        return "Неистовый " + self.enemy.name

    def roll_damage(self):
        first = self.enemy.roll_damage()
        second = self.enemy.roll_damage()
        return Hit(first.damage + second.damage, first.critical or second.critical)


class ArmoredEnemy(EnemyDecorator):
    @property
    def name(self):
        return "Бронированный " + self.enemy.name

    def receive_hit(self, amount):
        return self.enemy.receive_hit(max(1, amount // 2))
