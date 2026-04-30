def upsell(customer):
    if customer["usage"] > 10000:
        return "enterprise_plus"
    return "standard"
