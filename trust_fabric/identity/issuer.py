import base64
import json
import time


def issue(sub: str, tenant: str) -> str:
    if not sub or not tenant:
        raise ValueError("invalid identity")

    payload = {
        "sub": sub,
        "tenant": tenant,
        "iat": int(time.time()),
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()
