import torch
import torch.nn as nn


class Actor(nn.Module):
    def __init__(self, d_latent: int = 32, n_actions: int = 5) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_latent, 64),
            nn.ReLU(),
            nn.Linear(64, n_actions),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.net(z), dim=-1)
