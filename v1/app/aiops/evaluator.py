class Evaluator:
    def better(self, baseline: dict, canary: dict) -> bool:
        return (canary["lat"] <= baseline["latency"]) and (
            canary["err"] <= baseline["error_rate"]
        )
