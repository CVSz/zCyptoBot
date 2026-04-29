import subprocess
import time


class Canary:
    def __init__(self, service: str = "zeaz-api"):
        self.service = service

    def set_replicas(self, replicas: int):
        return subprocess.run(
            ["kubectl", "scale", f"deploy/{self.service}", f"--replicas={replicas}"],
            capture_output=True,
            text=True,
        )

    def rollout(self, image: str):
        return subprocess.run(
            [
                "kubectl",
                "set",
                "image",
                f"deployment/{self.service}",
                f"{self.service}={image}",
            ],
            capture_output=True,
            text=True,
        )

    def check(self, fetch_metrics, duration: int = 30, slo_target: dict | None = None):
        start = time.time()
        samples = []
        while time.time() - start < duration:
            samples.append(fetch_metrics())
            time.sleep(2)

        if not samples:
            return False, {"reason": "no_samples"}

        avg_lat = sum(sample["latency"] for sample in samples) / len(samples)
        avg_err = sum(sample["error_rate"] for sample in samples) / len(samples)

        ok = True
        if slo_target:
            if avg_lat > slo_target["latency"]:
                ok = False
            if avg_err > slo_target["error"]:
                ok = False

        return ok, {"lat": avg_lat, "err": avg_err}
