"""Billing computation helpers."""


def compute_bill(usage, base_fee=1000):
    """Compute hybrid enterprise bill from base fee + usage line items."""
    usage_cost = sum(u["value"] * u["price"] for u in usage)
    return base_fee + usage_cost
