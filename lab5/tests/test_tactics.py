from types import SimpleNamespace
from unittest.mock import create_autospec

import pytest
from labs.lab3.combat.battle import Battle
from labs.lab3.combat.combatant import Combatant
from labs.lab3.combat.hit import Hit
from labs.lab3.defense.damage import Damage
from labs.lab3.enemy.enemies import Enemy
from labs.lab3.tactic.strategies import (
    AggressiveTactic, BalancedTactic, CautiousTactic, Tactic)


def fighter(health, max_health=100):
    # stub: нужны только поля health / max_health
    return SimpleNamespace(health=health, max_health=max_health)


class FakeHero(Combatant):
    """Fake: упрощенный герой с постоянным уроном и неубиваемым здоровьем."""

    def __init__(self, damage=10):
        self.damage = damage

    @property
    def name(self):
        return "Фейк"

    @property
    def health(self):
        return 100

    def roll_damage(self):
        return Hit(self.damage)

    def receive_hit(self, amount):
        return Damage(amount)


class TestTactics:
    """Strategy: у каждой тактики свой множитель урона."""

    def test_balanced_is_always_one(self):
        assert BalancedTactic().choose_action(fighter(10), fighter(500), 3) == 1.0

    @pytest.mark.parametrize("hero_hp, enemy_hp, expected", [
        (50, 51, 1.5),   # враг здоровее
        (50, 50, 1.0),   # граница: поровну
        (50, 10, 1.0),   # враг слабее
    ])
    def test_aggressive_attacks_harder_against_healthier_enemy(self, hero_hp, enemy_hp, expected):
        assert AggressiveTactic().choose_action(fighter(hero_hp), fighter(enemy_hp), 1) == expected

    @pytest.mark.parametrize("hp, round_number, expected", [
        (39, 2, 0.5),    # мало здоровья, четный раунд
        (39, 3, 1.0),    # мало здоровья, нечетный раунд
        (40, 2, 1.0),    # граница 40%
        (100, 2, 1.0),   # здоров
    ])
    def test_cautious_weakens_attack_when_hurt_on_even_rounds(self, hp, round_number, expected):
        assert CautiousTactic().choose_action(fighter(hp), fighter(50), round_number) == expected

    def test_tactics_have_names(self):
        names = [BalancedTactic.name, AggressiveTactic.name, CautiousTactic.name]
        assert names == ["Баланс", "Натиск", "Осторожность"]


class TestBattleUsesTactic:
    def test_battle_asks_tactic_each_round_and_applies_multiplier(self):
        tactic = create_autospec(Tactic, instance=True)
        tactic.choose_action.return_value = 2.0
        hero = FakeHero(damage=10)
        enemy = Enemy("Крыса", 20, (1, 1), 5)

        report = Battle(hero, enemy, tactic).run()

        # 10 * 2.0 = 20 урона убивает врага с 20 HP за один раунд
        tactic.choose_action.assert_called_once_with(hero, enemy, 1)
        assert report["victory"] is True
        assert report["rounds"] == 1
        assert enemy.health == 0
