from app.aiops.bayesian_rca import BayesianRCA
from app.aiops.canary import Canary
from app.aiops.coordination import Coordinator
from app.aiops.cost_model import CostModel
from app.aiops.detector import Detector
from app.aiops.executor import Executor
from app.aiops.features_ctx import build_context
from app.aiops.online_learning import OnlineStore
from app.aiops.quorum import Quorum
from app.aiops.safeguards import Safeguards
from app.aiops.shadow import ShadowEngine
from app.aiops.adwin import ADWIN
from app.aiops.bandit_nl import NeuralTS
from app.aiops.sla import CostCeiling, SLA
from app.aiops.simulator import Simulator


class AIOpsV5:
    def __init__(self, fetch_metrics, region_id: str = "A"):
        self.fetch = fetch_metrics
        self.det = Detector()
        self.rca = BayesianRCA()
        self.policies = {}
        self.shadow = ShadowEngine()
        self.canary = Canary()
        self.exec = Executor()
        self.safe = Safeguards()
        self.coord = Coordinator(region_id)
        self.store = OnlineStore()
        self.cost = CostModel()
        self.quorum = Quorum(regions=("A", "B"), k=2)
        self.region = region_id
        self.drift = ADWIN(delta=0.002)
        self.sla = SLA()
        self.cost_ceiling = CostCeiling()
        self.simulator = Simulator()

    def step(self, tenant_id: str):
        metrics = self.fetch()
        metrics["tenant_tier"] = metrics.get("tenant_tier", "bronze")
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

        context = build_context(metrics, self.region)
        model = self.policies.setdefault(tenant_id, NeuralTS(d_in=context.shape[0], d_emb=16))

        if self.drift.update(metrics.get("latency", 0.0)):
            model.increase_exploration()
            model.reset_partial()

        action = model.select(context)

        sim = self.shadow.simulate([action])[0]
        _ = self.simulator.rollout(lambda st: action, steps=5)
        ok, _ = self.safe.allow(action, drawdown=0.0)
        if not ok:
            return {"blocked": action}

        if not self.coord.dedupe(action):
            return {"deduped": action}
        if not self.coord.acquire(action):
            return {"lease_busy": action}

        try:
            if action in ("rollback_deploy", "restart_kafka"):
                self.quorum.vote(action, self.region)
                if not self.quorum.approved(action):
                    return {"waiting_quorum": action}

            before = metrics
            if action in ("rollback_deploy", "restart_kafka"):
                okc, _ = self.canary.check(
                    self.fetch,
                    duration=30,
                    slo_target={"latency": 200, "error": 0.02},
                )
                if not okc:
                    self.exec.rollback_deploy()
                after = self.fetch()
            else:
                getattr(self.exec, action)()
                after = self.fetch()

            reward = self._reward(before, after, action, sim.risk, before.get("budget_left", 0.5), metrics.get("tenant_tier", "bronze"))
            model.update(action, context, reward)
            self.store.log(action, context.flatten().tolist(), reward)
            return {"action": action, "reward": reward}
        finally:
            self.coord.done(action)

    def _reward(self, before, after, action, risk, budget_left, tenant_tier):
        improvement = (before.get("latency", 0) - after.get("latency", 0)) / 100.0
        improvement += (before.get("error_rate", 0) - after.get("error_rate", 0)) * 10.0
        cost = self.cost.estimate(action, duration_min=5)
        if not self.cost_ceiling.allow(cost, budget_left):
            return -5.0

        penalty = self.cost.budget_penalty(budget_left)
        sla_rule = self.sla.get(str(tenant_tier))
        slo_penalty = 1.0 if (after.get("latency", 0) > sla_rule["latency"] or after.get("error_rate", 0) > sla_rule["error"]) else 0.0
        return improvement - (risk + cost + penalty + slo_penalty)
