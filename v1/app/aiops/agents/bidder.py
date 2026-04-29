"""Demand-side market bidder."""


class Bidder:
    def __init__(self, name: str) -> None:
        self.name = name

    def bid(self, state: dict, resource: str = "cpu") -> dict:
        latency = state.get("latency", 0.0)
        price = min(1.0, latency / 300.0)
        return {"agent": self.name, "res": resource, "price": round(price, 4), "qty": 1}
