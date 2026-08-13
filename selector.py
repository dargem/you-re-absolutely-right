import math, random

from typing import Generic, TypeVar

T = TypeVar("T")

# Weighted sampler, less likely to respond with recently selected items
class RandomSelector(Generic[T]):
    class Item:
        def __init__(self, val, turn):
            self.val = val
            self.turn = turn

    # Decrease lambda decay and it will prioritize old stuff
    def __init__(self, items: list[T], lambda_decay = 0.05, start_turn = -10):
        self.items: list = [self.Item(item, start_turn) for item in items]
        self.decay = lambda_decay
        self.turn = 0

    def choose(self) -> T:
        weights = [1 - 1 * math.exp(-self.decay * (self.turn - item.turn)) for item in self.items]
        choice = random.choices(self.items, weights=weights, k=1)[0]
        choice.turn = self.turn
        self.turn += 1

        return choice.val