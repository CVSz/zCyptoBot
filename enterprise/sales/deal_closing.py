"""Deal closing helper."""


def close(deal):
    """Return finalized contract metadata."""
    return {"contract": True, "value": deal["value"], "term": "12 months"}
