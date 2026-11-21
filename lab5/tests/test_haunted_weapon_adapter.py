from unittest.mock import create_autospec, patch

from labs.lab3.combat.combatant import Combatant
from labs.lab3.core.dice import Dice
from labs.lab3.enemy.enemies import HauntedWeapon

BOW = {"name": "Эльфийский лук", "damage": 14, "price": 90}


class TestHauntedWeaponAdapter:
    """Adapter: словарь-оружие превращается в врага (Combatant)."""

    def test_adapter_is_a_combatant(self):
        assert isinstance(HauntedWeapon(BOW), Combatant)

    def test_stats_are_derived_from_weapon(self):
        enemy = HauntedWeapon(BOW)

        assert enemy.name == "Одержимый Эльфийский лук"
        assert enemy.health == enemy.max_health == 70
        assert enemy.damage_range == (12, 16)
        assert enemy.experience_reward == 45

    def test_damage_roll_uses_weapon_range(self):
        enemy = HauntedWeapon(BOW)
        dice = create_autospec(Dice, instance=True)
        dice.roll.return_value = 13

        with patch("labs.lab3.enemy.enemies.Dice", return_value=dice):
            hit = enemy.roll_damage()

        dice.roll.assert_called_once_with(12, 16)
        assert hit.damage == 13

    def test_adapted_enemy_can_die(self):
        enemy = HauntedWeapon({"name": "Кинжал", "damage": 2, "price": 10})
        enemy.receive_hit(100)
        assert enemy.health == 0
        assert enemy.is_alive() is False
