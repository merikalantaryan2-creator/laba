from abc import ABC, abstractmethod


class Tactic(ABC):
    name = "Тактика"

    @abstractmethod
    def choose_action(self, hero, enemy, round_number):
        pass


class BalancedTactic(Tactic):
    name = "Баланс"

    def choose_action(self, hero, enemy, round_number):
        return 1.0


class AggressiveTactic(Tactic):
    name = "Натиск"

    def choose_action(self, hero, enemy, round_number):
        return 1.5 if enemy.health > hero.health else 1.0


class CautiousTactic(Tactic):
    name = "Осторожность"

    def choose_action(self, hero, enemy, round_number):
        return 0.5 if hero.health < hero.max_health * 0.4 and round_number % 2 == 0 else 1.0
