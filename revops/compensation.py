# path: revops/compensation.py

def commission(deal):
    rate = 0.1
    if deal["value"] > 100000:
        rate = 0.15
    return deal["value"] * rate
