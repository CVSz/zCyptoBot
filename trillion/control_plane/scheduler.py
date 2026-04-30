from typing import Dict, List


class Scheduler:
    """
    Chooses region/provider based on latency, cost, carbon, and SLO risk.
    """

    def choose(self, options: List[Dict]) -> Dict:
        # defensive: validate inputs
        valid = [o for o in options if all(k in o for k in ("latency", "cost", "carbon", "risk"))]
        if not valid:
            raise ValueError("no valid options")

        # weighted objective (tune via policy engine)
        def score(option):
            return (
                0.4 * option["cost"]
                + 0.3 * option["latency"]
                + 0.2 * option["carbon"]
                + 0.1 * option["risk"]
            )

        return min(valid, key=score)
