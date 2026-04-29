from collections import defaultdict


class CircuitBreaker:
    def __init__(self, threshold: float = 0.15):
        self.default_threshold = threshold
        self._threshold = defaultdict(lambda: self.default_threshold)

    def set(self, tenant: str, v: float):
        self._threshold[tenant] = v

    def get(self, tenant: str) -> float:
        return self._threshold[tenant]

    def tripped(self, tenant: str, dd: float) -> bool:
        return dd >= self._threshold[tenant]
