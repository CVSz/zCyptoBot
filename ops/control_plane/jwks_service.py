import time

JWKS = {}


def publish(issuer: str, kid: str, pub: str):
    JWKS.setdefault(issuer, {})[kid] = {"pub": pub, "ts": time.time()}


def get(issuer: str):
    return JWKS.get(issuer, {})
