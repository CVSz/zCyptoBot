import numpy as np
import torch

ACTIONS = ["scale", "hold", "shift", "restart"]


def onehot(a: str) -> torch.Tensor:
    v = np.zeros(len(ACTIONS), dtype=np.float32)
    v[ACTIONS.index(a)] = 1
    return torch.tensor(v, dtype=torch.float32)


class Planner:
    def __init__(self, wm):
        self.wm = wm

    def plan(self, state: torch.Tensor) -> str:
        best_a, best_val = None, -1e9
        for a in ACTIONS:
            a_oh = onehot(a)
            next_s = self.wm(state, a_oh)
            reward = -float(next_s[0])
            if reward > best_val:
                best_val = reward
                best_a = a
        return best_a or "hold"
