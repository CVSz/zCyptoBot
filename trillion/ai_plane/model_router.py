from typing import Dict, List


class ModelRouter:
    """
    Routes to best model/provider based on latency/cost/quality.
    """

    def route(self, candidates: List[Dict]) -> Dict:
        # validate
        cands = [c for c in candidates if all(k in c for k in ("latency", "cost", "quality"))]
        if not cands:
            raise ValueError("no candidates")

        def score(candidate):
            # maximize quality, minimize cost/latency
            return (1.0 * candidate["quality"]) - (0.5 * candidate["cost"] + 0.3 * candidate["latency"])

        return max(cands, key=score)
