from __future__ import annotations

import numpy as np

from rl.replay import ReplayBuffer

ACTIONS = ["scale", "hold", "shift", "restart"]


class RLAgent:
    def __init__(self, epsilon: float = 0.1, lr: float = 0.1) -> None:
        self.q: dict[tuple[float, ...], np.ndarray] = {}
        self.epsilon = epsilon
        self.lr = lr
        self.replay = ReplayBuffer()

    @staticmethod
    def key(state: dict[str, float]) -> tuple[float, ...]:
        return tuple(round(v, 2) for v in state.values())

    def _ensure(self, key: tuple[float, ...]) -> None:
        if key not in self.q:
            self.q[key] = np.zeros(len(ACTIONS))

    def act(self, state: dict[str, float]) -> str:
        k = self.key(state)
        self._ensure(k)

        if np.random.rand() < self.epsilon:
            return str(np.random.choice(ACTIONS))

        return ACTIONS[int(np.argmax(self.q[k]))]

    def update(self, state: dict[str, float], action: str, reward: float) -> None:
        k = self.key(state)
        self._ensure(k)
        idx = ACTIONS.index(action)
        self.q[k][idx] += self.lr * (reward - self.q[k][idx])
        self.replay.add(state.copy(), action, reward)

    def replay_train(self, n: int = 64) -> None:
        for s, a, r in self.replay.sample(n):
            self.update(dict(s), a, r)
