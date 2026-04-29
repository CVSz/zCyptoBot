from __future__ import annotations

import random


class TS:
    def __init__(self, k: int = 3) -> None:
        self.a = [1] * k
        self.b = [1] * k

    def select(self) -> int:
        samples = [random.betavariate(self.a[i], self.b[i]) for i in range(len(self.a))]
        return max(range(len(samples)), key=lambda i: samples[i])

    def update(self, i: int, reward: float) -> None:
        if reward > 0:
            self.a[i] += 1
        else:
            self.b[i] += 1
