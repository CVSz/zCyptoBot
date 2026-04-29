import random
from collections.abc import Mapping


class ReplayBuffer:
    def __init__(self, size: int = 10000) -> None:
        self.size = size
        self.buf: list[tuple[Mapping[str, float], str, float]] = []

    def add(self, s: Mapping[str, float], a: str, r: float) -> None:
        self.buf.append((s, a, r))
        if len(self.buf) > self.size:
            self.buf.pop(0)

    def sample(self, n: int = 64) -> list[tuple[Mapping[str, float], str, float]]:
        return random.sample(self.buf, min(n, len(self.buf)))
