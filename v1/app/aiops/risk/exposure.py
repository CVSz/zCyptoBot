class Exposure:
    def check(self, total_cost: float, threshold: float = 10) -> bool:
        return total_cost < threshold
