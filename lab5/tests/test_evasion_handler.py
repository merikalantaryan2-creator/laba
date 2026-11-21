from unittest.mock import create_autospec, patch

from labs.lab3.core.dice import Dice
from labs.lab3.defense.damage import Damage
from labs.lab3.defense.handlers import DamageHandler, EvasionHandler


def make_dice(result):
    dice = create_autospec(Dice, instance=True)
    dice.chance.return_value = result
    return dice


class TestEvasionHandler:
    def test_evades_and_stops_chain(self):
        dice = make_dice(True)
        next_handler = create_autospec(DamageHandler, instance=True)
        handler = EvasionHandler(0.3)
        handler.set_next(next_handler)
        damage = Damage(40)

        # подменяем имя Dice там, где его использует обработчик
        with patch("labs.lab3.defense.handlers.Dice", return_value=dice) as singleton:
            handler.handle(damage)
            singleton.assert_called_once_with()

        assert damage.amount == 0
        assert damage.evaded is True
        dice.chance.assert_called_once_with(0.3)
        assert next_handler.mock_calls == []

    def test_forwards_damage_when_roll_fails(self):
        dice = make_dice(False)
        next_handler = create_autospec(DamageHandler, instance=True)
        handler = EvasionHandler(0.3)
        handler.set_next(next_handler)
        damage = Damage(40)

        with patch("labs.lab3.defense.handlers.Dice", return_value=dice):
            handler.handle(damage)

        assert damage.amount == 40
        assert damage.evaded is False
        dice.chance.assert_called_once_with(0.3)
        next_handler.handle.assert_called_once_with(damage)
        assert next_handler.handle.call_args.args[0] is damage
