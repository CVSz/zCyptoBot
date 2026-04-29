import numpy as np

from app.aiops.autoscale import AutoScaler
from app.aiops.bandit import LinUCB
from app.aiops.bayesian_rca import BayesianRCA
from app.aiops.canary import Canary
from app.aiops.coordination import Coordinator
from app.aiops.cost_model import CostModel
from app.aiops.detector import Detector
from app.aiops.executor import Executor
from app.aiops.online_learning import OnlineStore
from app.aiops.quorum import Quorum
from app.aiops.safeguards import Safeguards
from app.aiops.shadow import ShadowEngine


class AIOpsV4:
    def __init__(self, fetch_metrics, region_id="A"):
        self.fetch = fetch_metrics
        self.det = Detector()
        self.rca = BayesianRCA()
        self.bandit = LinUCB(d=6, alpha=0.8)
        self.shadow = ShadowEngine()
        self.canary = Canary()
        self.exec = Executor()
        self.safe = Safeguards()
        self.coord = Coordinator(region_id)
        self.store = OnlineStore()
        self.cost = CostModel()
        self.quorum = Quorum(regions=("A", "B"), k=2)
        self.scale = AutoScaler()
        self.store.replay(self.bandit, limit=5000)

    def _context(self, metrics):
        return np.array(
            [
                min(metrics.get("latency", 0) / 300.0, 2.0),
                min(metrics.get("error_rate", 0) / 0.05, 2.0),
                min(metrics.get("kafka_lag", 0) / 50.0, 2.0),
                1.0 if self.coord.region == "A" else 0.0,
                metrics.get("hour", 12) / 24.0,
                metrics.get("budget_left", 0.5),
            ]
        ).reshape(-1, 1)

    def step(self):
        metrics = self.fetch()
        self.det.ingest(metrics)
        anomalies = self.det.anomalies()
        if not anomalies:
            return {"status": "healthy"}

        evidence = {
            "latency_high": any(a["metric"] == "latency" for a in anomalies),
            "error_high": any(a["metric"] == "error_rate" for a in anomalies),
            "lag_high": any(a["metric"] == "kafka_lag" for a in anomalies),
        }
        _ = self.rca.infer(evidence)

        context = self._context(metrics)
        action = self.bandit.select(context)
        sim = self.shadow.simulate([action])[0]
        ok, _ = self.safe.allow(action, drawdown=0.0)
        if not ok:
            return {"blocked": action}

        if not self.coord.dedupe(action):
            return {"deduped": action}
        if not self.coord.acquire(action):
            return {"lease_busy": action}

        try:
            if action in ("rollback_deploy", "restart_kafka"):
                self.quorum.vote(action, self.coord.region)
                if not self.quorum.approved(action):
                    return {"waiting_quorum": action}

            before = metrics
            if action in ("scale_api", "scale_consumers"):
                replicas = self.scale.decide(
                    before.get("latency", 0),
                    before.get("kafka_lag", 0),
                    before.get("budget_left", 0.5),
                )
                deploy = "zeaz-api" if action == "scale_api" else "zeaz-consumer"
                self.scale.set_replicas(deploy, replicas)
                after = self.fetch()
                reward = self._reward(before, after, action, sim.risk, before.get("budget_left", 0.5))
                self.bandit.update(action, context, reward)
                self.store.log(action, context.flatten().tolist(), reward)
                return {"action": action, "replicas": replicas}

            if action in ("rollback_deploy", "restart_kafka"):
                okc, _ = self.canary.check(self.fetch, duration=30, slo_target={"latency": 200, "error": 0.02})
                if not okc:
                    self.exec.rollback_deploy()
                after = self.fetch()
                reward = self._reward(before, after, action, sim.risk, before.get("budget_left", 0.5))
                self.bandit.update(action, context, reward)
                self.store.log(action, context.flatten().tolist(), reward)
                return {"action": action, "status": "promoted" if okc else "aborted"}

            result = getattr(self.exec, action)()
            after = self.fetch()
            reward = self._reward(before, after, action, sim.risk, before.get("budget_left", 0.5))
            self.bandit.update(action, context, reward)
            self.store.log(action, context.flatten().tolist(), reward)
            return {"action": action, "rc": result.returncode}
        finally:
            self.coord.done(action)

    def _reward(self, before, after, action, risk, budget_left):
        improvement = (before.get("latency", 0) - after.get("latency", 0)) / 100.0
        improvement += (before.get("error_rate", 0) - after.get("error_rate", 0)) * 10.0
        cost = self.cost.estimate(action, duration_min=5)
        penalty = self.cost.budget_penalty(budget_left)
        slo_penalty = 1.0 if (after.get("latency", 0) > 200 or after.get("error_rate", 0) > 0.02) else 0.0
        return improvement - (risk + cost + penalty + slo_penalty)
