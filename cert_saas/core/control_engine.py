import time

from .policy_engine import evaluate

STATE = []


def run(tenant_id: str, resources: list):
    for r in resources:
        res = evaluate(r)
        STATE.append({"tenant": tenant_id, "res": res, "ts": time.time()})
    return STATE
