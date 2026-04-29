"""AML checks for suspicious transfers."""


def suspicious(tx) -> bool:
    return tx["amount"] > 10000
