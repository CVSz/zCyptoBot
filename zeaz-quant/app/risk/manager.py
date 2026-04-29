class RiskManager:
    def __init__(self, max_risk: float, max_position: float) -> None:
        self.max_risk = max_risk
        self.max_position = max_position
        self.position = 0.0

    def validate(self, signal: str, price: float) -> float:
        _ = (signal, price)
        size = self.max_position * self.max_risk

        if abs(self.position + size) > self.max_position:
            return 0.0

        return size

    def update(self, signal: str, size: float) -> None:
        if signal == "LONG":
            self.position += size
        elif signal == "SHORT":
            self.position -= size
