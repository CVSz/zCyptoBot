import subprocess


class AutoScaler:
    def set_replicas(self, deploy: str, replicas: int):
        return subprocess.run(["kubectl", "scale", f"deploy/{deploy}", f"--replicas={replicas}"])

    def decide(self, latency_ms, lag, budget_left_ratio):
        base = 3 if (latency_ms > 200 or lag > 20) else 2
        if budget_left_ratio < 0.3:
            base = max(1, base - 1)
        return base
