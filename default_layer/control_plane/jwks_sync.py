CACHE = {}


def update(issuer: str, jwks: dict):
    CACHE[issuer] = jwks


def get(issuer: str):
    return CACHE.get(issuer, {})
