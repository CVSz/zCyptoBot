def add_demand(queue, tenant, units, max_price):
    queue.append({
        "tenant": tenant,
        "units": units,
        "max_price": max_price,
    })
    return queue
