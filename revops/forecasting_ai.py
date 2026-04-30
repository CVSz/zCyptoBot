# path: revops/forecasting_ai.py

def weighted_pipeline(deals):
    return sum(d["value"] * d["probability"] for d in deals)

def forecast_next_month(history):
    if len(history) < 2:
        return history[-1] if history else 0
    growth = (history[-1] - history[-2]) / max(history[-2],1)
    return history[-1] * (1 + growth)
