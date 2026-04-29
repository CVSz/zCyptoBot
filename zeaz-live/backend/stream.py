import random


def update_state(state):
    state["latency"] *= random.uniform(0.95, 1.05)
    state["error"] *= random.uniform(0.95, 1.05)
    state["load"] *= random.uniform(0.95, 1.05)
    return state
