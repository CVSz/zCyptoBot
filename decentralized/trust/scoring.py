SCORE = {}


def update(node_id: str, success: bool, latency: float):
    s = SCORE.get(node_id, 0.5)
    s += 0.05 if success else -0.1
    if latency > 300:
        s -= 0.05
    SCORE[node_id] = max(0.0, min(1.0, s))


def get(node_id: str) -> float:
    return SCORE.get(node_id, 0.5)
