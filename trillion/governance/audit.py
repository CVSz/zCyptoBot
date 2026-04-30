import time

AUDIT_LOG = []


def log(event: dict):
    AUDIT_LOG.append({**event, "ts": time.time()})


def query(filter_fn):
    return [e for e in AUDIT_LOG if filter_fn(e)]
