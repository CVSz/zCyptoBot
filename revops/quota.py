# path: revops/quota.py

def assign_quota(rep, base=50000):
    if rep["role"] == "senior":
        return base * 2
    return base
