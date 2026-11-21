import random

import pytest
from labs.lab3.core.dice import Dice


@pytest.fixture(autouse=True)
def fixed_seed():
    random.seed(2026)


class TestDice:
    def test_rolls_stay_within_bounds(self):
        low, high = 1, 6
        for _ in range(100):
            assert low <= Dice().roll(low, high) <= high

    def test_equal_bounds_return_only_value(self):
        assert Dice().roll(7, 7) == 7

    def test_handles_certain_outcomes(self):
        for _ in range(100):
            assert Dice().chance(0.0) is False
            assert Dice().chance(1.0) is True

    def test_same_seed_repeats_sequence(self):
        random.seed(42)
        first = [Dice().roll(1, 100) for _ in range(10)]
        random.seed(42)
        repeated = [Dice().roll(1, 100) for _ in range(10)]
        assert first == repeated
