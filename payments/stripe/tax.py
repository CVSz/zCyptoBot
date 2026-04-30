"""Basic tax helpers."""


def apply_tax(amount, country="TH"):
    """Apply country-specific tax percentage to an amount."""
    if country == "TH":
        return amount * 1.07
    return amount
