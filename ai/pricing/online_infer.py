import torch


def predict(model, demand, supply, latency, trust):
    x = torch.tensor([demand, supply, latency, trust], dtype=torch.float32)
    return float(model(x))
