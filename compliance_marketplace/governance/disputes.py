def resolve(order, outcome):
    if outcome not in {"refund", "release"}:
        raise ValueError("invalid outcome")
    order["status"] = outcome
    return order
