REGISTRY = {}


def register(name, version, risk):
    if risk not in {"low", "high"}:
        raise ValueError("invalid risk")
    REGISTRY[name] = {
        "version": version,
        "risk": risk,
    }
