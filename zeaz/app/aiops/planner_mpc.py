from collections import Counter

import numpy as np
import torch

ACTIONS = ["scale_api", "restart_pods", "rollback_deploy", "scale_consumers", "restart_kafka"]


def onehot(a: int, n: int) -> np.ndarray:
    v = np.zeros((n,), dtype=np.float32)
    v[a] = 1.0
    return v


class MPCPlanner:
    def __init__(self, wm, horizon: int = 5, samples: int = 64, topk: int = 8) -> None:
        self.wm = wm
        self.H = horizon
        self.N = samples
        self.K = topk

    def plan(self, x) -> str:
        with torch.no_grad():
            z0 = self.wm.enc(torch.tensor(x, dtype=torch.float32))
            seqs = np.random.randint(0, len(ACTIONS), size=(self.N, self.H))
            returns = []

            for seq in seqs:
                z = z0.clone()
                reward_total = 0.0
                for action_id in seq:
                    action_onehot = torch.tensor(onehot(int(action_id), len(ACTIONS)), dtype=torch.float32)
                    z = self.wm.dyn(z, action_onehot)
                    reward_total += float(self.wm.rwd(z))
                returns.append(reward_total)

            idx = np.argsort(returns)[-self.K :]
            best = seqs[idx]
            first_actions = [int(seq[0]) for seq in best]
            best_first_action = Counter(first_actions).most_common(1)[0][0]
            return ACTIONS[best_first_action]
