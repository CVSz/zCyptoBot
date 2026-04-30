def segment_price(base: float, segment: str, volume: int) -> float:
    """Apply differentiated pricing based on segment and usage volume."""
    if segment == "enterprise_ai":
        return base * 1.2  # premium for performance/SLA
    if segment == "startup":
        return base * 0.7  # land with lower entry
    if volume > 1_000_000:
        return base * 0.8
    return base
