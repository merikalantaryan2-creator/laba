from dataclasses import dataclass


@dataclass
class Damage:
    amount: int
    evaded: bool = False
    absorbed: int = 0

    def reduce_to(self, amount: int) -> None:
        self.amount = max(0, amount)

    def evade(self) -> None:
        self.amount = 0
        self.evaded = True

    def absorb(self, value: int) -> None:
        actual = min(self.amount, max(0, value))
        self.amount -= actual
        self.absorbed += actual
