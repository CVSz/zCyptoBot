SCORE = {}


def update(node_id: str, success: bool):
    SCORE[node_id] = SCORE.get(node_id, 0.5)
    SCORE[node_id] += 0.05 if success else -0.1
    SCORE[node_id] = max(0.0, min(1.0, SCORE[node_id]))


def get(node_id: str) -> float:
    return SCORE.get(node_id, 0.5)
