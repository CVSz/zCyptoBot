import base64
import hashlib
import json
import time


def _b64(x: bytes) -> str:
    return base64.urlsafe_b64encode(x).decode().rstrip("=")


def issue(sub: str, iss: str, tenant: str, region: str, att: dict, ttl=600):
    if not all([sub, iss, tenant, region, att]):
        raise ValueError("invalid input")

    now = int(time.time())
    payload = {
        "sub": sub,
        "iss": iss,
        "tenant": tenant,
        "region": region,
        "att": hashlib.sha256(json.dumps(att, sort_keys=True).encode()).hexdigest(),
        "iat": now,
        "exp": now + ttl,
        "jti": _b64(hashlib.sha256(f"{sub}{now}".encode()).digest())[:16],
    }
    token = _b64(json.dumps(payload, sort_keys=True).encode())
    return token
