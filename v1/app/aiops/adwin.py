import math
from collections import deque


class ADWIN:
    """Minimal Adaptive Windowing drift detector for streaming scalar values."""

    def __init__(self, delta: float = 0.002, min_subwindow: int = 5):
        self.delta = delta
        self.min_subwindow = min_subwindow
        self.window = deque()

    def update(self, value: float) -> bool:
        self.window.append(float(value))
        changed = False
        n = len(self.window)
        if n < 2 * self.min_subwindow:
            return changed

        values = list(self.window)
        for split in range(self.min_subwindow, n - self.min_subwindow + 1):
            w0 = values[:split]
            w1 = values[split:]
            n0, n1 = len(w0), len(w1)
            m0 = sum(w0) / n0
            m1 = sum(w1) / n1
            eps = math.sqrt((1.0 / (2.0 * n0)) * math.log(2.0 / self.delta))
            if abs(m0 - m1) > eps:
                self.window = deque(w1)
                changed = True
                break

        return changed
