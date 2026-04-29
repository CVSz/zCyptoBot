class CircuitBreaker:
    def __init__(self, threshold: int = 5) -> None:
        self.failures = 0
        self.threshold = threshold

    def record(self, ok: bool) -> None:
        if ok:
            self.failures = 0
        else:
            self.failures += 1

    def open(self) -> bool:
        return self.failures > self.threshold
