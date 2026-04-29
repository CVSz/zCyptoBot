class PricingEngine:
    def __init__(self):
        self.base_price = 0.2

    def price(self, load, demand, carbon_score):
        return self.base_price + 0.5 * load + 0.3 * demand + 0.2 * (carbon_score / 500)

    def surge(self, latency):
        return 1.5 if latency > 200 else 1.0
