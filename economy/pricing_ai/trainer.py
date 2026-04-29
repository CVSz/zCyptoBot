"""Training helpers for pricing AI."""


def train_step(ai, metrics):
    reward = 1.0 - metrics["latency"] / 300
    ai.update(reward)
