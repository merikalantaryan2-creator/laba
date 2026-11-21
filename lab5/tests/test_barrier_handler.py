import pytest
from labs.lab3.defense.damage import Damage
from labs.lab3.defense.handlers import BarrierHandler


def damage_cases():
    # (входящий урон, поглощено, прошло) для барьера прочностью 30:
    # ноль, меньше, граница-1, граница, граница+1, больше
    return [(0, 0, 0), (10, 10, 0), (29, 29, 0), (30, 30, 0), (31, 30, 1), (40, 30, 10)]


class TestBarrierHandler:
    @pytest.mark.parametrize("incoming, absorbed, remaining", damage_cases())
    def test_handles_damage_boundaries(self, incoming, absorbed, remaining):
        # Arrange
        barrier = BarrierHandler(30)
        damage = Damage(incoming)

        # Act
        barrier.handle(damage)

        # Assert
        assert damage.absorbed == absorbed
        assert damage.amount == remaining

    def test_returns_same_damage_object(self):
        damage = Damage(10)
        assert BarrierHandler(5).handle(damage) is damage

    def test_barrier_points_apply_to_each_hit(self):
        # текущая реализация не расходует прочность: каждый удар поглощается заново
        barrier = BarrierHandler(5)
        first, second = Damage(20), Damage(20)

        barrier.handle(first)
        barrier.handle(second)

        assert (first.absorbed, first.amount) == (5, 15)
        assert (second.absorbed, second.amount) == (5, 15)


class TestDamage:
    def test_absorb_ignores_negative_value(self):
        damage = Damage(10)
        damage.absorb(-5)
        assert (damage.amount, damage.absorbed) == (10, 0)

    def test_reduce_to_never_goes_below_zero(self):
        damage = Damage(10)
        damage.reduce_to(-3)
        assert damage.amount == 0

    def test_evade_zeroes_damage_and_marks_flag(self):
        damage = Damage(10)
        damage.evade()
        assert damage.amount == 0
        assert damage.evaded is True
