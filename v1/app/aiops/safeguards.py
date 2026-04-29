import time

from app.guardrails.circuit import CircuitBreaker
from app.guardrails.kill_switch import KillSwitch


class Safeguards:
    def __init__(self, max_actions_per_min: int = 3):
        self.cb = CircuitBreaker(0.2)
        self.ks = KillSwitch()
        self.max_actions = max_actions_per_min
        self._window_epoch = int(time.time() // 60)
        self._counter = 0

    def _refresh_window(self):
        current_epoch = int(time.time() // 60)
        if current_epoch != self._window_epoch:
            self._window_epoch = current_epoch
            self._counter = 0

    def allow(self, action: str, drawdown: float):
        del action
        self._refresh_window()
        if self.ks.is_on():
            return False, "kill_switch"
        if self.cb.tripped("public", drawdown):
            return False, "circuit_tripped"
        if self._counter >= self.max_actions:
            return False, "rate_limited"
        self._counter += 1
        return True, "ok"
