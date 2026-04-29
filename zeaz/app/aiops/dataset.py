import random


class ReplayBuffer:
    def __init__(self, cap: int = 100000) -> None:
        self.cap = cap
        self.buf = []

    def add(self, state, action, reward, next_state) -> None:
        self.buf.append((state, action, reward, next_state))
        if len(self.buf) > self.cap:
            self.buf.pop(0)

    def sample(self, n: int = 256):
        return random.sample(self.buf, min(n, len(self.buf)))
