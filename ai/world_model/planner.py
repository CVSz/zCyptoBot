import torch


def plan(model, state, steps=5):
    h = None
    s = state
    total = 0

    for _ in range(steps):
        s, h = model(s, h)
        reward = -s[0]  # minimize latency
        total += reward

    return total
