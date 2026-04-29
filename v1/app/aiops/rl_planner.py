import random
from collections import defaultdict

ACTIONS = [
    "scale_api",
    "restart_pods",
    "rollback_deploy",
    "scale_consumers",
    "restart_kafka",
]


class RLPlanner:
    def __init__(self, alpha: float = 0.2, gamma: float = 0.9, eps: float = 0.2):
        self.Q = defaultdict(lambda: {action: 0.0 for action in ACTIONS})
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps

    def _state(self, slo_ok: bool, high_lag: bool) -> str:
        return f"{int(slo_ok)}:{int(high_lag)}"

    def select(self, slo_ok: bool, high_lag: bool) -> str:
        state = self._state(slo_ok, high_lag)
        if random.random() < self.eps:
            return random.choice(ACTIONS)
        return max(self.Q[state], key=self.Q[state].get)

    def update(
        self,
        slo_ok: bool,
        high_lag: bool,
        action: str,
        reward: float,
        next_slo_ok: bool,
        next_high_lag: bool,
    ):
        state = self._state(slo_ok, high_lag)
        next_state = self._state(next_slo_ok, next_high_lag)
        best_next = max(self.Q[next_state].values())
        self.Q[state][action] += self.alpha * (
            reward + self.gamma * best_next - self.Q[state][action]
        )
