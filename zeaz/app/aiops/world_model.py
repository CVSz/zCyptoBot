import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, d_in: int = 8, d_latent: int = 32) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, 64),
            nn.ReLU(),
            nn.Linear(64, d_latent),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class Dynamics(nn.Module):
    def __init__(self, d_latent: int = 32, n_actions: int = 5) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_latent + n_actions, 64),
            nn.ReLU(),
            nn.Linear(64, d_latent),
        )

    def forward(self, z: torch.Tensor, a_onehot: torch.Tensor) -> torch.Tensor:
        x = torch.cat([z, a_onehot], dim=-1)
        return self.net(x)


class RewardHead(nn.Module):
    def __init__(self, d_latent: int = 32) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_latent, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)


class WorldModel(nn.Module):
    def __init__(self, d_in: int = 8, d_latent: int = 32, n_actions: int = 5) -> None:
        super().__init__()
        self.enc = Encoder(d_in=d_in, d_latent=d_latent)
        self.dyn = Dynamics(d_latent=d_latent, n_actions=n_actions)
        self.rwd = RewardHead(d_latent=d_latent)

    def forward(self, x: torch.Tensor, a_onehot: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        z = self.enc(x)
        z_next = self.dyn(z, a_onehot)
        r = self.rwd(z_next)
        return z, z_next, r
