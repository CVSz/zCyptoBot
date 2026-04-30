def incentive(partner_type: str):
    if partner_type == "si":
        return {"rev_share": 0.3}
    if partner_type == "hyperscaler":
        return {"co_sell": True}
    if partner_type == "government":
        return {"discount": 0.2}
    return {}
