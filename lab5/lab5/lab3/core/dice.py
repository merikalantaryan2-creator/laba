import random


class Dice:
    # единый генератор случайных чисел
    def roll(self, low: int, high: int) -> int:
        return random.randint(low, high)

    def chance(self, probability: float) -> bool:
        return random.random() < probability
