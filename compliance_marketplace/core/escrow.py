ESCROW = {}


def hold(order_id, amount):
    if amount <= 0:
        raise ValueError("invalid amount")
    ESCROW[order_id] = amount


def release(order_id):
    return ESCROW.pop(order_id, 0)
