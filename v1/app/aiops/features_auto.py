from __future__ import annotations

import torch
import torch.nn as nn


class FeatureExtractor(nn.Module):
    def __init__(self, d_in: int = 8, d_out: int = 16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, 32),
            nn.ReLU(),
            nn.Linear(32, d_out),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def feature_importance(z: torch.Tensor) -> float:
    return torch.abs(z).mean().item()
