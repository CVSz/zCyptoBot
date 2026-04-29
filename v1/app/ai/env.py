import gymnasium as gym


class TradingEnv(gym.Env):
    def __init__(self, data):
        self.data = data
        self.step_idx = 0
        self.balance = 10000
        self.position = 0  # -1 short, 0 flat, 1 long

    def reset(self, seed=None, options=None):
        self.step_idx = 0
        self.balance = 10000
        self.position = 0
        return self._get_obs(), {}

    def _get_obs(self):
        return self.data[self.step_idx]

    def step(self, action):
        price = self.data[self.step_idx][0]

        reward = 0
        if action == 1:  # LONG
            self.position = 1
        elif action == 2:  # SHORT
            self.position = -1

        if self.step_idx > 0:
            prev_price = self.data[self.step_idx - 1][0]
            reward = self.position * (price - prev_price)

        self.step_idx += 1
        done = self.step_idx >= len(self.data) - 1

        return self._get_obs(), reward, done, False, {}
