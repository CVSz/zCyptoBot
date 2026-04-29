from __future__ import annotations


class SafetyAgent:
    def __init__(self, max_error_rate: float = 0.05):
        self.max_error_rate = max_error_rate

    def allow(self, action: str, metrics: dict) -> bool:
        _ = action
        return metrics.get("error_rate", 0.0) <= self.max_error_rate
