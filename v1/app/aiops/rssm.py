from __future__ import annotations

import torch
import torch.nn as nn


class RSSM(nn.Module):
    """Compact recurrent state-space model used by Dreamer-style planning."""

    def __init__(self, d_latent: int = 32, d_action: int = 5):
        super().__init__()
        self.d_latent = d_latent
        self.d_action = d_action
        self.rnn = nn.GRUCell(d_latent + d_action, d_latent)
        self.prior = nn.Linear(d_latent, d_latent)
        self.post = nn.Linear(d_latent * 2, d_latent)

    def forward(self, z: torch.Tensor, a: torch.Tensor, encoded_obs: torch.Tensor | None = None):
        x = torch.cat([z, a], dim=-1)
        h = self.rnn(x, z)
        prior = self.prior(h)
        if encoded_obs is None:
            post = prior
        else:
            post = self.post(torch.cat([h, encoded_obs], dim=-1))
        return h, prior, post
