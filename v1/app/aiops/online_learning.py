import json

try:
    from clickhouse_driver import Client
except Exception:  # pragma: no cover
    Client = None


class OnlineStore:
    def __init__(self):
        self.db = Client(host="clickhouse") if Client else None

    def log(self, action, context, reward):
        if not self.db:
            return
        self.db.execute("INSERT INTO aiops_events VALUES", [(action, json.dumps(context), float(reward))])

    def replay(self, bandit, limit=10000):
        if not self.db:
            return
        rows = self.db.execute(
            "SELECT action, context, reward FROM aiops_events LIMIT %(l)s", {"l": int(limit)}
        )
        import numpy as np

        for action, ctx_json, reward in rows:
            x = np.array(json.loads(ctx_json)).reshape(-1, 1)
            bandit.update(action, x, reward)
