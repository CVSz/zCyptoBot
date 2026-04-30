from .pricing import price


def generate_invoice(tenant, usage, cost):
    revenue = price(usage)
    margin = revenue - cost

    return {
        "tenant": tenant,
        "revenue": revenue,
        "cost": cost,
        "margin": margin,
    }
