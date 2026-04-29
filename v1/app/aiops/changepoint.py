from collections import deque


class SlidingWindow:
    def __init__(self, n: int = 200):
        self.buf = deque(maxlen=n)

    def add(self, x: float):
        self.buf.append(x)

    def mean(self):
        if not self.buf:
            return 0.0
        return sum(self.buf) / len(self.buf)


class CUSUM:
    def __init__(self, k: float = 0.5, h: float = 5.0):
        self.k = k
        self.h = h
        self.g = 0.0
        self.reset_points = 0

    def update(self, x: float, mu: float):
        score = x - mu - self.k
        self.g = max(0.0, self.g + score)
        if self.g > self.h:
            self.g = 0.0
            self.reset_points += 1
            return True
        return False
