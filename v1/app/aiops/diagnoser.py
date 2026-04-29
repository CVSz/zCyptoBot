from app.aiops.knowledge import RULES


class Diagnoser:
    def diagnose(self, anomalies: list):
        plans = []
        for anomaly in anomalies:
            actions = RULES.get(anomaly["metric"], [])
            plans.append({"metric": anomaly["metric"], "actions": actions})
        return plans
