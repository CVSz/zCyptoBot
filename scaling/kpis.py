# path: scaling/kpis.py


def metrics(arr, customers, churn, expansion):
    return {
        "ARR": arr,
        "Customers": customers,
        "Churn": churn,
        "Expansion Revenue": expansion,
    }
