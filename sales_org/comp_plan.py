# path: sales_org/comp_plan.py


def commission(deal):
    if deal["value"] > 200000:
        return deal["value"] * 0.15
    return deal["value"] * 0.1
