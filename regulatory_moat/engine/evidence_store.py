import hashlib
import json
import time

STORE = []


def put(evidence: dict):
    blob = json.dumps(evidence, sort_keys=True).encode()
    h = hashlib.sha256(blob).hexdigest()
    rec = {"hash": h, "evidence": evidence, "ts": time.time()}
    STORE.append(rec)
    return rec


def query(f):
    return [r for r in STORE if f(r)]
