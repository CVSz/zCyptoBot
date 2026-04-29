"""Simple autonomous pricing model."""

import numpy as np


class PricingAI:
    def __init__(self) -> None:
        self.weights = np.random.rand(4)

    def price(self, demand: float, supply: float, latency: float, trust: float) -> float:
        x = np.array([demand, supply, latency, trust])
        return float(np.dot(self.weights, x))

    def update(self, reward: float) -> None:
        self.weights += 0.01 * reward
