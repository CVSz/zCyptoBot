def apply_tax(amount, country="TH"):
    if country == "TH":
        return amount * 1.07
    return amount
