import numpy as np

ACTIONS = ["scale_api", "restart_pods", "rollback_deploy", "scale_consumers", "restart_kafka"]


class LinUCB:
    def __init__(self, d: int = 6, alpha: float = 0.8):
        self.alpha = alpha
        self.A = {action: np.eye(d) for action in ACTIONS}
        self.b = {action: np.zeros((d, 1)) for action in ACTIONS}

    def select(self, x: np.ndarray) -> str:
        scores = {}
        for action in ACTIONS:
            a_inv = np.linalg.inv(self.A[action])
            theta = a_inv @ self.b[action]
            score = float((theta.T @ x) + self.alpha * np.sqrt(x.T @ a_inv @ x))
            scores[action] = score
        return max(scores, key=scores.get)

    def update(self, action: str, x: np.ndarray, reward: float):
        self.A[action] += x @ x.T
        self.b[action] += reward * x
