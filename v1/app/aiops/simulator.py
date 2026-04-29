import random


class Simulator:
    def simulate_step(self, state, action: str):
        lat = float(state["latency"])
        err = float(state["error"])

        if action == "scale_api":
            lat *= 0.8
        elif action == "restart_pods":
            err *= 0.7
        elif action == "rollback_deploy":
            err *= 0.5
        elif action == "restart_kafka":
            lat *= 1.2
            err *= 1.3

        lat *= random.uniform(0.95, 1.05)
        err *= random.uniform(0.95, 1.05)
        return {"latency": lat, "error": err}

    def rollout(self, policy, steps: int = 50):
        state = {"latency": 200.0, "error": 0.02}
        logs = []

        for _ in range(steps):
            action = policy(state)
            next_state = self.simulate_step(state, action)
            reward = (state["latency"] - next_state["latency"]) + (state["error"] - next_state["error"]) * 10.0
            logs.append((state.copy(), action, reward))
            state = next_state

        return logs
