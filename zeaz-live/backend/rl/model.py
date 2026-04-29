import torch
import torch.nn as nn

ACTIONS = ["scale", "hold", "shift", "restart"]


class PolicyNet(nn.Module):
    def __init__(self, d_in: int = 3, d_out: int = len(ACTIONS)):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, 64),
            nn.ReLU(),
            nn.Linear(64, d_out),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.net(x), dim=-1)
