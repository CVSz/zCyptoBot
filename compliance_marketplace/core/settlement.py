def split(amount, partner_pct=0.7):
    if not (0 <= partner_pct <= 1):
        raise ValueError("pct 0..1")
    return {
        "partner": amount * partner_pct,
        "platform": amount * (1 - partner_pct),
    }
