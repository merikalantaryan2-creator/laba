from unittest.mock import create_autospec, patch

import pytest
from labs.lab3.core.dice import Dice
from labs.lab3.defense.damage import Damage
from labs.lab3.defense.handlers import (
    ArmorHandler, BarrierHandler, DamageHandler, EvasionHandler)
from labs.lab3.hero.hero import Hero


class RecordingHandler(DamageHandler):
    """Spy: записывает, что его вызвали, и не меняет урон."""

    def __init__(self, label, journal):
        super().__init__()
        self.label = label
        self.journal = journal

    def apply(self, damage):
        self.journal.append(self.label)


class TestChainOfResponsibility:
    def test_request_passes_through_all_handlers_in_order(self):
        journal = []
        first = RecordingHandler("первый", journal)
        first.set_next(RecordingHandler("второй", journal)).set_next(
            RecordingHandler("третий", journal))

        first.handle(Damage(10))

        assert journal == ["первый", "второй", "третий"]

    def test_set_next_returns_next_handler_for_fluent_linking(self):
        first, second = ArmorHandler(0.1), BarrierHandler(1)
        assert first.set_next(second) is second

    def test_real_chain_combines_all_effects(self):
        # 30 урона: уклонение 0% -> броня 30% (30*0.7=21) -> барьер 10 -> 11
        chain = EvasionHandler(0.0)
        chain.set_next(ArmorHandler(0.3)).set_next(BarrierHandler(10))

        result = chain.handle(Damage(30))

        assert result.amount == 11
        assert result.absorbed == 10
        assert result.evaded is False

    def test_stops_when_damage_already_zero(self):
        journal = []
        armor = ArmorHandler(1.0)  # съедает весь урон
        armor.set_next(RecordingHandler("после брони", journal))

        result = armor.handle(Damage(25))

        assert result.amount == 0
        assert journal == []

    def test_armor_without_reduction_keeps_damage(self):
        assert ArmorHandler(0.0).handle(Damage(25)).amount == 25


class TestHeroDefenseChain:
    """Hero собирает цепочку Уклонение 10% -> Броня 10% -> Барьер 5."""

    def _dice(self, result):
        dice = create_autospec(Dice, instance=True)
        dice.chance.return_value = result
        return dice

    def test_hero_takes_damage_through_whole_chain(self):
        hero = Hero("Артур")
        with patch("labs.lab3.defense.handlers.Dice", return_value=self._dice(False)):
            result = hero.receive_hit(40)

        # 40 * 0.9 = 36, барьер поглощает 5 -> 31
        assert result.amount == 31
        assert hero.health == 100 - 31

    def test_hero_evades_and_keeps_health(self):
        hero = Hero("Артур")
        with patch("labs.lab3.defense.handlers.Dice", return_value=self._dice(True)):
            result = hero.receive_hit(40)

        assert result.evaded is True
        assert hero.health == hero.max_health

    def test_health_never_drops_below_zero(self):
        hero = Hero("Артур")
        with patch("labs.lab3.defense.handlers.Dice", return_value=self._dice(False)):
            hero.receive_hit(10_000)
        assert hero.health == 0
        assert hero.is_alive() is False
