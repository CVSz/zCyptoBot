import numpy as np

ACTIONS = ["scale_api", "restart_pods", "rollback_deploy", "scale_consumers", "restart_kafka"]


class LinTS_NS:
    def __init__(self, d: int = 8, v: float = 0.25, lam: float = 1.0, discount: float = 0.98):
        self.d = d
        self.v2 = v * v
        self.lam = lam
        self.gamma = discount
        self.A = {action: lam * np.eye(d) for action in ACTIONS}
        self.b = {action: np.zeros((d, 1)) for action in ACTIONS}

    def _posterior(self, action: str):
        a_inv = np.linalg.inv(self.A[action])
        mu = a_inv @ self.b[action]
        sigma = self.v2 * a_inv
        return mu, sigma

    def select(self, x: np.ndarray) -> str:
        best_action = ACTIONS[0]
        best_val = float("-inf")
        for action in ACTIONS:
            mu, sigma = self._posterior(action)
            theta = np.random.multivariate_normal(mean=mu.flatten(), cov=sigma).reshape(-1, 1)
            val = float((theta.T @ x).item())
            if val > best_val:
                best_val = val
                best_action = action
        return best_action

    def update(self, action: str, x: np.ndarray, reward: float):
        self.A[action] = self.gamma * self.A[action] + x @ x.T
        self.b[action] = self.gamma * self.b[action] + reward * x
