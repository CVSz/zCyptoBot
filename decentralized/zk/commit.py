import hashlib
import json
import time


def commit(payload: dict, salt: str) -> str:
    blob = json.dumps({"p": payload, "s": salt, "t": int(time.time())}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()
