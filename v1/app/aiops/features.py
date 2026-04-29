from collections import deque
import time


class SlidingStats:
    def __init__(self, n: int = 60):
        self.n = n
        self.buf = deque(maxlen=n)

    def add(self, x: float):
        self.buf.append((time.time(), x))

    def mean_std(self):
        if not self.buf:
            return 0.0, 0.0
        vals = [v for _, v in self.buf]
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / max(1, len(vals))
        return mean, var**0.5
