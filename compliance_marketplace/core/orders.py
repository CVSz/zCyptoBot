ORDERS = []


def create(user, item_id):
    o = {"user": user, "item": item_id, "status": "pending"}
    ORDERS.append(o)
    return o
