from app.aiops.canary import Canary
from app.aiops.detector import Detector
from app.aiops.diagnoser import Diagnoser
from app.aiops.evaluator import Evaluator
from app.aiops.executor import Executor
from app.aiops.safeguards import Safeguards
from app.aiops.shadow import ShadowEngine
from app.aiops.slo_planner import SLO, SLOPlanner


class AIOpsV2:
    def __init__(self, fetch_metrics):
        self.detector = Detector()
        self.diagnoser = Diagnoser()
        self.planner = SLOPlanner()
        self.shadow = ShadowEngine()
        self.canary = Canary()
        self.evaluator = Evaluator()
        self.executor = Executor()
        self.safeguards = Safeguards()
        self.fetch_metrics = fetch_metrics

    def step(self, drawdown: float = 0.0):
        metric = self.fetch_metrics()
        self.detector.ingest(metric)
        anomalies = self.detector.anomalies()
        if not anomalies:
            return {"status": "healthy"}

        diagnoses = self.diagnoser.diagnose(anomalies)
        actions = sorted({action for diagnosis in diagnoses for action in diagnosis["actions"]})

        shadow_results = self.shadow.simulate(actions)
        chosen = self.planner.choose(
            shadow_results,
            SLO(latency_ms_p95=200, error_rate=0.01, budget=0.6),
        )

        approved = []
        for action in chosen:
            ok, _ = self.safeguards.allow(action, drawdown=drawdown)
            if ok:
                approved.append(action)

        baseline = self.fetch_metrics()
        results = []

        for action in approved:
            if action in ("rollback_deploy", "restart_kafka"):
                self.canary.set_replicas(2)
                self.canary.rollout("yourrepo/zeaz:canary")
                ok, stats = self.canary.check(
                    self.fetch_metrics,
                    duration=30,
                    slo_target={"latency": 200, "error": 0.02},
                )
                if ok and self.evaluator.better(baseline, stats):
                    self.canary.set_replicas(4)
                    results.append((action, "promoted"))
                else:
                    self.executor.rollback_deploy()
                    results.append((action, "aborted"))
            else:
                fn = getattr(self.executor, action, None)
                if fn:
                    response = fn()
                    results.append((action, response.returncode))

        return {"actions": approved, "results": results}
