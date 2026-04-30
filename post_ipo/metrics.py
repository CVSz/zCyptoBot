def metrics(arr: float, growth: float, margin: float, retention: float) -> dict:
    """Return a compact public-market KPI snapshot."""
    return {
        "ARR": arr,
        "Growth": growth,
        "GrossMargin": margin,
        "NetRetention": retention,
    }
