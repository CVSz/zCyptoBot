"""Dynamic pricing primitives."""


def dynamic_price(load: float, base: float = 0.3) -> float:
    bounded = max(0.0, min(1.0, load))
    return round(base + 0.5 * bounded, 4)
