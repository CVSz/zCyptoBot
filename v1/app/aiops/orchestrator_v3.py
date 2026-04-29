from app.aiops.bayesian_rca import BayesianRCA
from app.aiops.canary import Canary
from app.aiops.coordination import Coordinator
from app.aiops.detector import Detector
from app.aiops.executor import Executor
from app.aiops.rl_planner import RLPlanner
from app.aiops.safeguards import Safeguards
from app.aiops.shadow import ShadowEngine


class AIOpsV3:
    def __init__(self, fetch_metrics, region_id: str = "A"):
        self.fetch = fetch_metrics
        self.det = Detector()
        self.rca = BayesianRCA()
        self.rl = RLPlanner()
        self.shadow = ShadowEngine()
        self.canary = Canary()
        self.exec = Executor()
        self.safe = Safeguards()
        self.coord = Coordinator(region_id)

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
        causes = self.rca.infer(evidence)
        top_cause = causes[0][0]

        slo_ok = metrics.get("latency", 0) < 200 and metrics.get("error_rate", 0) < 0.02
        high_lag = metrics.get("kafka_lag", 0) > 10
        action = self.rl.select(slo_ok, high_lag)

        sim = self.shadow.simulate([action])[0]

        ok, reason = self.safe.allow(action, drawdown=0.0)
        if not ok:
            return {"blocked": action, "reason": reason, "cause": top_cause}

        if not self.coord.dedupe(action):
            return {"deduped": action, "cause": top_cause}

        if not self.coord.acquire(action):
            return {"lease_busy": action, "cause": top_cause}

        try:
            if action in ("rollback_deploy", "restart_kafka"):
                base = self.fetch()
                okc, stats = self.canary.check(
                    self.fetch,
                    duration=30,
                    slo_target={"latency": 200, "error": 0.02},
                )
                reward = self._reward(base, stats, sim.risk)
                self.rl.update(
                    slo_ok,
                    high_lag,
                    action,
                    reward,
                    stats["lat"] < 200 and stats["err"] < 0.02,
                    high_lag,
                )
                if okc:
                    return {"action": action, "status": "promoted", "cause": top_cause}

                self.exec.rollback_deploy()
                return {"action": action, "status": "aborted", "cause": top_cause}

            resp = getattr(self.exec, action)()
            after = self.fetch()
            reward = self._reward(metrics, after, sim.risk)
            self.rl.update(
                slo_ok,
                high_lag,
                action,
                reward,
                after.get("latency", 0) < 200 and after.get("error_rate", 0) < 0.02,
                after.get("kafka_lag", 0) > 10,
            )
            return {"action": action, "rc": resp.returncode, "cause": top_cause}
        finally:
            self.coord.done(action)

    def _reward(self, before: dict, after: dict, risk: float) -> float:
        improvement = (before.get("latency", 0) - after.get("latency", 0)) + (
            before.get("error_rate", 0) - after.get("error_rate", 0)
        ) * 100
        cost = 0.2
        penalty = 1.0 if (after.get("latency", 0) > 200 or after.get("error_rate", 0) > 0.02) else 0.0
        return improvement - (risk + cost + penalty)
