import numpy as np


def build_context(metrics: dict, region_id: str) -> np.ndarray:
    return np.array(
        [
            min(metrics.get("latency", 0) / 300.0, 2.0),
            min(metrics.get("error_rate", 0) / 0.05, 2.0),
            min(metrics.get("kafka_lag", 0) / 50.0, 2.0),
            1.0 if region_id == "A" else 0.0,
            metrics.get("hour", 12) / 24.0,
            metrics.get("budget_left", 0.5),
            metrics.get("tenant_tier", 1) / 3.0,
            metrics.get("traffic_norm", 0.5),
        ]
    ).reshape(-1, 1)
