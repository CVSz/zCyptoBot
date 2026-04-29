class RiskEngine:
    def __init__(self, max_risk: float, max_pos: float):
        self.max_risk = max_risk
        self.max_pos = max_pos
        self.pos = 0.0

    def validate(self, sig: str) -> float:
        size = self.max_pos * self.max_risk
        direction = 1 if sig == "LONG" else -1
        if abs(self.pos + (direction * size)) > self.max_pos:
            return 0.0
        return size

    def update(self, sig: str, size: float) -> None:
        if sig == "LONG":
            self.pos += size
        else:
            self.pos -= size
