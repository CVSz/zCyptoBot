from collections import defaultdict


class Budget:
    def __init__(self, default_limit: float):
        self.default_limit = default_limit
        self._limit = defaultdict(lambda: self.default_limit)

    def set(self, tenant: str, v: float):
        self._limit[tenant] = v

    def get(self, tenant: str) -> float:
        return self._limit[tenant]
