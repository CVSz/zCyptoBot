from __future__ import annotations

import torch
import torch.nn as nn


class Actor(nn.Module):
    def __init__(self, d_latent: int = 32, n_actions: int = 5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_latent, 64),
            nn.ReLU(),
            nn.Linear(64, n_actions),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.net(z), dim=-1)


class Critic(nn.Module):
    def __init__(self, d_latent: int = 32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_latent, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)
