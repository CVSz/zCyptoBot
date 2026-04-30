import time

REVOKED = {}


def revoke(jti: str, ttl_sec: int = 600):
    REVOKED[jti] = time.time() + ttl_sec


def is_revoked(jti: str) -> bool:
    exp = REVOKED.get(jti)
    return exp is not None and exp > time.time()
