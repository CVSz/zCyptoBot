import numpy as np
import torch

from app.ai.agent import DQNAgent
from app.ai.env import TradingEnv


def train():
    data = np.random.rand(1000, 4).astype(np.float32)

    env = TradingEnv(data)
    agent = DQNAgent(state_dim=4, action_dim=3)

    for _ in range(50):
        state, _ = env.reset()
        done = False

        while not done:
            action = agent.act(state)
            next_state, reward, done, _, _ = env.step(action)

            agent.store((state, action, reward, next_state, done))
            agent.train_step()

            state = next_state

    torch.save(agent.model.state_dict(), "app/models/policy.pt")


if __name__ == "__main__":
    train()
