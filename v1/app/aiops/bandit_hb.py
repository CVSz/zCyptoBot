from collections import defaultdict

import numpy as np

ACTIONS = ["scale_api", "restart_pods", "rollback_deploy", "scale_consumers", "restart_kafka"]


class HBLinear:
    def __init__(self, d: int = 8, v: float = 0.25, lam: float = 1.0):
        self.d = d
        self.v2 = v * v
        self.lam = lam
        self.Ag = {action: lam * np.eye(d) for action in ACTIONS}
        self.bg = {action: np.zeros((d, 1)) for action in ACTIONS}
        self.At = defaultdict(lambda: {action: lam * np.eye(d) for action in ACTIONS})
        self.bt = defaultdict(lambda: {action: np.zeros((d, 1)) for action in ACTIONS})

    def _post(self, A, b):
        a_inv = np.linalg.inv(A)
        mu = a_inv @ b
        sigma = self.v2 * a_inv
        return mu, sigma

    def _fuse(self, mu_t, s_t, mu_g, s_g):
        p_t = np.linalg.inv(s_t)
        p_g = np.linalg.inv(s_g)
        s = np.linalg.inv(p_t + p_g)
        mu = s @ (p_t @ mu_t + p_g @ mu_g)
        return mu, s

    def select(self, tenant: str, x: np.ndarray) -> str:
        best_action = ACTIONS[0]
        best_val = float("-inf")
        for action in ACTIONS:
            mu_t, s_t = self._post(self.At[tenant][action], self.bt[tenant][action])
            mu_g, s_g = self._post(self.Ag[action], self.bg[action])
            mu, s = self._fuse(mu_t, s_t, mu_g, s_g)
            theta = np.random.multivariate_normal(mu.flatten(), s).reshape(-1, 1)
            val = float((theta.T @ x).item())
            if val > best_val:
                best_val = val
                best_action = action
        return best_action

    def update(self, tenant: str, action: str, x: np.ndarray, reward: float, discount: float = 0.98):
        self.At[tenant][action] = discount * self.At[tenant][action] + x @ x.T
        self.bt[tenant][action] = discount * self.bt[tenant][action] + reward * x
        self.Ag[action] = discount * self.Ag[action] + x @ x.T
        self.bg[action] = discount * self.bg[action] + reward * x
