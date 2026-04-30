class CostModel:
    def score(self, region):
        return (
            0.5 * region["cost"]
            + 0.3 * region["latency"]
            + 0.2 * region["carbon"]
        )
