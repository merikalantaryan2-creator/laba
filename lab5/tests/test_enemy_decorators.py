from unittest.mock import create_autospec, patch

import pytest
from labs.lab3.combat.hit import Hit
from labs.lab3.defense.damage import Damage
from labs.lab3.enemy.decorators import ArmoredEnemy, LegendaryEnemy, WindfuryEnemy
from labs.lab3.enemy.enemies import Enemy
from labs.lab3.core.dice import Dice


def inner_enemy():
    """Мок исходного врага: проверяем, что декоратор делегирует ему вызовы."""
    enemy = create_autospec(Enemy, instance=True)
    enemy.name = "Гоблин"
    enemy.experience_reward = 40
    return enemy


class TestEnemyDecorators:
    def test_legendary_doubles_damage_and_reward(self):
        inner = inner_enemy()
        inner.roll_damage.return_value = Hit(10, False)
        enemy = LegendaryEnemy(inner)

        hit = enemy.roll_damage()

        assert hit == Hit(20, False)
        assert enemy.experience_reward == 80
        assert enemy.name == "Легендарный Гоблин"
        inner.roll_damage.assert_called_once_with()

    def test_windfury_attacks_twice_and_sums_damage(self):
        inner = inner_enemy()
        inner.roll_damage.side_effect = [Hit(5, False), Hit(7, True)]
        enemy = WindfuryEnemy(inner)

        hit = enemy.roll_damage()

        assert hit == Hit(12, True)
        assert inner.roll_damage.call_count == 2
        assert enemy.name == "Неистовый Гоблин"

    @pytest.mark.parametrize("incoming, passed", [(20, 10), (9, 4), (1, 1), (0, 1)])
    def test_armored_halves_incoming_hit(self, incoming, passed):
        inner = inner_enemy()
        enemy = ArmoredEnemy(inner)

        enemy.receive_hit(incoming)

        inner.receive_hit.assert_called_once_with(passed)

    def test_decorator_delegates_unmodified_members(self):
        inner = inner_enemy()
        inner.health = 33
        inner.max_health = 50
        inner.is_alive.return_value = True
        enemy = ArmoredEnemy(inner)

        assert enemy.health == 33
        assert enemy.max_health == 50
        assert enemy.is_alive() is True
        assert enemy.experience_reward == 40

    def test_all_stacked_decorators_apply_their_behavior(self):
        base = Enemy("Гоблин", 50, (8, 14), 40)
        enemy = ArmoredEnemy(LegendaryEnemy(WindfuryEnemy(base)))
        dice = create_autospec(Dice, instance=True)
        dice.roll.return_value = 10

        with patch("labs.lab3.enemy.enemies.Dice", return_value=dice):
            hit = enemy.roll_damage()
        result = enemy.receive_hit(30)

        # Неистовый: 10 + 10, Легендарный: *2
        assert hit.damage == 40
        assert dice.roll.call_count == 2
        # Бронированный: 30 // 2 = 15 урона дошло до исходного врага
        assert isinstance(result, Damage) and result.amount == 15
        assert base.health == 35
        assert enemy.experience_reward == 80
        assert enemy.name == "Бронированный Легендарный Неистовый Гоблин"
