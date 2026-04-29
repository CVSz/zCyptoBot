import numpy as np

ACTIONS = ["scale_api", "restart_pods", "rollback_deploy", "scale_consumers", "restart_kafka"]


class RandomFourierEmbedding:
    """Lightweight non-linear embedding via random Fourier features."""

    def __init__(self, d_in: int = 8, d_out: int = 16, sigma: float = 1.0, seed: int = 7):
        rng = np.random.default_rng(seed)
        self.w = rng.normal(0.0, 1.0 / sigma, size=(d_out, d_in))
        self.b = rng.uniform(0.0, 2.0 * np.pi, size=(d_out, 1))
        self.scale = np.sqrt(2.0 / d_out)

    def transform(self, x: np.ndarray) -> np.ndarray:
        vec = x.reshape(-1, 1)
        proj = self.w @ vec + self.b
        return self.scale * np.cos(proj)


class NeuralTS:
    """Non-linear contextual Thompson Sampling using an embedding + linear posterior."""

    def __init__(self, d_in: int = 8, d_emb: int = 16, v: float = 0.25, lam: float = 1.0):
        self.embedder = RandomFourierEmbedding(d_in=d_in, d_out=d_emb)
        self.v2 = v * v
        self.A = {a: lam * np.eye(d_emb) for a in ACTIONS}
        self.b = {a: np.zeros((d_emb, 1)) for a in ACTIONS}

    def embed(self, x: np.ndarray) -> np.ndarray:
        return self.embedder.transform(x)

    def select(self, x: np.ndarray) -> str:
        z = self.embed(x)
        best_action = ACTIONS[0]
        best_value = float("-inf")

        for action in ACTIONS:
            a_inv = np.linalg.inv(self.A[action])
            mu = a_inv @ self.b[action]
            sigma = self.v2 * a_inv
            theta = np.random.multivariate_normal(mu.flatten(), sigma).reshape(-1, 1)
            val = float((theta.T @ z).item())
            if val > best_value:
                best_value = val
                best_action = action

        return best_action

    def update(self, action: str, x: np.ndarray, reward: float):
        z = self.embed(x)
        self.A[action] += z @ z.T
        self.b[action] += reward * z

    def increase_exploration(self, factor: float = 1.2):
        self.v2 *= factor

    def reset_partial(self, shrink: float = 0.5):
        for action in ACTIONS:
            self.A[action] = np.eye(self.A[action].shape[0]) + shrink * (self.A[action] - np.eye(self.A[action].shape[0]))
            self.b[action] *= shrink
