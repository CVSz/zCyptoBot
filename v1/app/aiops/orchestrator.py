import time

from app.aiops.detector import Detector
from app.aiops.diagnoser import Diagnoser
from app.aiops.executor import Executor
from app.aiops.planner import Planner
from app.aiops.safeguards import Safeguards
from app.aiops.state import Incident


class AIOps:
    def __init__(self):
        self.detector = Detector()
        self.diagnoser = Diagnoser()
        self.planner = Planner()
        self.executor = Executor()
        self.safeguards = Safeguards()
        self.incident = Incident()

    def ingest_metrics(self, metric: dict):
        self.detector.ingest(metric)

    def step(self, drawdown: float = 0.0):
        anomalies = self.detector.anomalies()
        if not anomalies:
            self.incident.transition("healthy")
            return {"status": "ok"}

        self.incident.transition("detecting", anomalies)
        diagnoses = self.diagnoser.diagnose(anomalies)
        actions = self.planner.plan(diagnoses)

        self.incident.transition("mitigating", actions)
        results = []
        for action in actions:
            allowed, reason = self.safeguards.allow(action, drawdown)
            if not allowed:
                results.append((action, f"blocked:{reason}"))
                continue
            fn = getattr(self.executor, action, None)
            if fn:
                response = fn()
                results.append((action, response.returncode))
        self.incident.transition("recovering", results)
        return {"anomalies": anomalies, "actions": actions, "results": results}


def run_loop(fetch_metrics, interval: int = 5):
    aiops = AIOps()
    while True:
        metric = fetch_metrics()
        aiops.ingest_metrics(metric)
        aiops.step()
        time.sleep(interval)
