"""Enterprise dashboard metric calculator."""


def compute_metrics(usage_cost, zeaz_cost, revenue):
    """Compute cost, savings, ROI, and margin metrics."""
    savings = usage_cost - zeaz_cost
    roi = (savings / zeaz_cost) if zeaz_cost else 0

    return {
        "original_cost": usage_cost,
        "zeaz_cost": zeaz_cost,
        "savings": savings,
        "roi": roi,
        "margin": revenue - zeaz_cost,
    }
