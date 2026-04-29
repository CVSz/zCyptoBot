from collections import defaultdict

BAL = defaultdict(float)


def create_account(a: str):
    BAL[a] += 0.0


def credit(a: str, amount: float):
    BAL[a] += amount


def debit(a: str, amount: float):
    if BAL[a] < amount:
        raise ValueError("insufficient balance")
    BAL[a] -= amount


def balance(a: str) -> float:
    return BAL[a]
