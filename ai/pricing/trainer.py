import torch

from ai.pricing.model import PricingModel

model = PricingModel()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)


def train_step(features, reward):
    x = torch.tensor(features, dtype=torch.float32)
    pred = model(x)

    loss = (pred - reward) ** 2

    opt.zero_grad()
    loss.backward()
    opt.step()
    return float(loss.detach())
