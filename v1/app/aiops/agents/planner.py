from __future__ import annotations

import torch


class PlannerAgent:
    def __init__(self, actor, action_space: list[str]):
        self.actor = actor
        self.action_space = action_space

    def act(self, z: torch.Tensor) -> str:
        probs = self.actor(z)
        idx = int(probs.argmax(dim=-1).item())
        return self.action_space[idx]
