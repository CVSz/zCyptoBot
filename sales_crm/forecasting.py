from sales_crm.models import DEALS


def forecast_revenue() -> float:
    values = [deal.value * deal.probability for deal in DEALS]
    return sum(values)


def forecast_growth(history):
    if len(history) < 2:
        return 0
    return (history[-1] - history[0]) / max(history[0], 1)
