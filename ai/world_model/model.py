import torch.nn as nn


class WorldModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Linear(4, 32)
        self.dynamics = nn.GRU(32, 32, batch_first=True)
        self.head = nn.Linear(32, 4)

    def forward(self, x, h=None):
        z = self.encoder(x)
        out, h = self.dynamics(z.unsqueeze(0), h)
        return self.head(out.squeeze(0)), h
