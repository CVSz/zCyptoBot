# path: scaling_50m/metrics.py


def metrics(arr, partners, expansion):
    return {
        "ARR": arr,
        "Partner Revenue %": partners,
        "Expansion %": expansion,
    }
