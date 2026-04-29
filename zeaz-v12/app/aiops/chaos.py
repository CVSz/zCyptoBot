import random


class ChaosController:
    """Inject low-rate chaos only when current SLO status is healthy."""

    def inject(self, metrics):
        if metrics["latency"] < 150 and metrics.get("error", 0) < 0.01:
            if random.random() < 0.1:
                return "kill_pod"
        return None
