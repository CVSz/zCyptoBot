import hashlib
import json
import time

STORE = []


def put(e):
    blob = json.dumps(e, sort_keys=True).encode()
    h = hashlib.sha256(blob).hexdigest()
    rec = {"hash": h, "evidence": e, "ts": time.time()}
    STORE.append(rec)
    return rec
