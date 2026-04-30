from .collector import USAGE


def get_usage(tenant=None):
    if tenant is None:
        return list(USAGE)
    return [u for u in USAGE if u["tenant"] == tenant]
