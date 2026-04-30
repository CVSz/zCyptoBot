# path: revops/board_metrics.py

def metrics(arr, burn, new_arr, churn):
    return {
        "ARR": arr,
        "Net New ARR": new_arr,
        "Burn": burn,
        "Churn Rate": churn,
        "Burn Multiple": burn / max(new_arr,1)
    }
