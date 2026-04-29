"""In-memory credit ledger for marketplace settlement."""

from collections import defaultdict

BAL = defaultdict(float)


def mint(user: str, amount: float) -> None:
    """Add credits to a user balance."""
    BAL[user] += amount


def spend(user: str, amount: float) -> None:
    """Deduct credits from a user balance if sufficient."""
    if BAL[user] < amount:
        raise ValueError("insufficient credits")
    BAL[user] -= amount


def transfer(frm: str, to: str, amount: float) -> None:
    """Move credits from one account to another."""
    spend(frm, amount)
    BAL[to] += amount


def balance(user: str) -> float:
    """Return current credit balance for a user."""
    return BAL[user]
