import time


class ControlEngine:
    def __init__(self):
        self.state = []

    def run(self, resources, policy_engine, controls):
        for r in resources:
            res = policy_engine.evaluate(r, controls)
            self.state.append({"resource": r.get("id"), "result": res, "ts": time.time()})
        return self.state
