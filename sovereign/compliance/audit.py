import time

AUDIT = []


def log(event: dict):
    AUDIT.append({**event, "ts": time.time()})


def query(filter_fn):
    return [e for e in AUDIT if filter_fn(e)]
