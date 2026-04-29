import numpy as np


def feature_dict(metrics: dict, region_id: str) -> dict:
    return {
        "lat": min(metrics.get("latency", 0) / 300.0, 2.0),
        "err": min(metrics.get("error_rate", 0) / 0.05, 2.0),
        "lag": min(metrics.get("kafka_lag", 0) / 50.0, 2.0),
        "region_a": 1.0 if region_id == "A" else 0.0,
        "hour": metrics.get("hour", 12) / 24.0,
        "budget": metrics.get("budget_left", 0.5),
        "tier": metrics.get("tenant_tier", 1) / 3.0,
        "traffic": metrics.get("traffic_norm", 0.5),
    }


def build_context(metrics: dict, region_id: str) -> np.ndarray:
    feats = feature_dict(metrics, region_id)
    return np.array(list(feats.values())).reshape(-1, 1)
