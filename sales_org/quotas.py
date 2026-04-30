# path: sales_org/quotas.py


def quota(rep_level):
    if rep_level == "enterprise":
        return 1000000  # $1M ARR / rep
    return 300000
