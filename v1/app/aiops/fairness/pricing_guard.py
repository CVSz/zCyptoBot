class PricingGuard:
    def clamp(self, price: float) -> float:
        return min(price, 1.5)
