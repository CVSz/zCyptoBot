"""Core KPI helpers for the $1B ARR hyperscale plan."""


def metrics(arr, retention, expansion):
    return {
        "ARR": arr,
        "Net Retention": retention,
        "Expansion": expansion,
    }
