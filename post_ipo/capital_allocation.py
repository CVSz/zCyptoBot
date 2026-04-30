def allocate(cash: float) -> dict:
    """Distribute available capital across core strategic buckets."""
    return {
        "R&D": cash * 0.3,
        "M&A": cash * 0.3,
        "Sales": cash * 0.25,
        "Reserve": cash * 0.15,
    }
