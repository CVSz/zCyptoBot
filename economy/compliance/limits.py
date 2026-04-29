"""Per-user transfer limit checks."""

LIMITS = {"daily": 5000}


def check(user: str, amount: float) -> bool:
    del user
    return amount < LIMITS["daily"]
