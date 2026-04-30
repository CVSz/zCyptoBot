# path: partners/incentives.py


def partner_commission(deal):
    if deal["tier"] == "platinum":
        return deal["value"] * 0.3
    return deal["value"] * 0.2
