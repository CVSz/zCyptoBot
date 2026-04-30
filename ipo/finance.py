# path: ipo/finance.py

def unit_economics(revenue, cost, cac):
    margin = revenue - cost
    ltv = revenue * 3
    return {
        "margin": margin,
        "LTV": ltv,
        "CAC": cac,
        "LTV/CAC": ltv / max(cac, 1)
    }

def burn_multiple(burn, new_arr):
    return burn / max(new_arr, 1)
