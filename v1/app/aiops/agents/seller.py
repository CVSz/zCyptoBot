"""Supply-side market seller."""

from app.aiops.market.pricing import dynamic_price


class Seller:
    def __init__(self, name: str) -> None:
        self.name = name

    def ask(self, capacity: int, load: float, resource: str = "cpu") -> dict:
        return {
            "agent": self.name,
            "res": resource,
            "price": dynamic_price(load),
            "qty": capacity,
        }
