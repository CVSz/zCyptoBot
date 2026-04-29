import random


class ABRouter:
    def __init__(self):
        self.alloc = {}

    def set(self, tenant: str, weights: dict):
        self.alloc[tenant] = weights

    def route(self, tenant: str):
        weights = self.alloc.get(tenant, {"A": 1.0})
        r = random.random()
        cum = 0.0
        for variant, weight in weights.items():
            cum += weight
            if r <= cum:
                return variant
        return list(weights.keys())[-1]
