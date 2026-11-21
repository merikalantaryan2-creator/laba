from unittest.mock import create_autospec, patch

import pytest
from labs.lab3.core.dice import Dice
from labs.lab3.enemy.decorators import ArmoredEnemy, LegendaryEnemy, WindfuryEnemy
from labs.lab3.enemy.enemies import Dragon, Enemy, HauntedWeapon
from labs.lab3.world.locations import (
    Crypt, DragonLair, Forest, HauntedManor, Location)


def patched_dice(**kwargs):
    dice = create_autospec(Dice, instance=True)
    dice.chance.configure_mock(**kwargs)
    return dice


def patch_dice(dice):
    # decorate_enemy берет Dice из модуля locations
    return patch("labs.lab3.world.locations.Dice", return_value=dice)


class TestLocationFactoryMethod:
    """Factory Method: каждая локация сама решает, какого врага создать."""

    @pytest.mark.parametrize("location, enemy_type, name", [
        (Forest(), Enemy, "Гоблин"),
        (Crypt(), Enemy, "Скелет"),
        (DragonLair(), Dragon, "Дракон"),
        (HauntedManor(), HauntedWeapon, "Одержимый Эльфийский лук"),
    ])
    def test_each_location_creates_its_own_enemy(self, location, enemy_type, name):
        with patch_dice(patched_dice(return_value=False)):
            enemy = location.create_enemy()

        assert type(enemy) is enemy_type
        assert enemy.name == name

    def test_forest_and_crypt_differ_in_stats(self):
        with patch_dice(patched_dice(return_value=False)):
            goblin, skeleton = Forest().create_enemy(), Crypt().create_enemy()

        assert (goblin.max_health, goblin.experience_reward) == (50, 40)
        assert (skeleton.max_health, skeleton.experience_reward) == (65, 60)

    def test_every_call_creates_new_object(self):
        with patch_dice(patched_dice(return_value=False)):
            forest = Forest()
            assert forest.create_enemy() is not forest.create_enemy()

    def test_base_location_has_no_factory_implementation(self):
        with pytest.raises(NotImplementedError):
            Location("Пустота").create_enemy()

    def test_location_keeps_its_name(self):
        assert Forest().name == "Мистический лес"
        assert DragonLair().name == "Логово дракона"


class TestEnemyDecoration:
    def test_no_decorators_when_all_rolls_fail(self):
        dice = patched_dice(return_value=False)
        with patch_dice(dice):
            enemy = Forest().create_enemy()

        assert type(enemy) is Enemy
        assert dice.chance.call_count == 3

    def test_all_decorators_when_all_rolls_succeed(self):
        dice = patched_dice(return_value=True)
        with patch_dice(dice):
            enemy = Forest().create_enemy()

        assert isinstance(enemy, ArmoredEnemy)
        assert enemy.name == "Бронированный Неистовый Легендарный Гоблин"
        dice.chance.assert_any_call(0.35)
        dice.chance.assert_any_call(0.30)

    def test_only_legendary_when_first_roll_succeeds(self):
        dice = patched_dice(side_effect=[True, False, False])
        with patch_dice(dice):
            enemy = Crypt().create_enemy()

        assert isinstance(enemy, LegendaryEnemy)
        assert enemy.name == "Легендарный Скелет"
