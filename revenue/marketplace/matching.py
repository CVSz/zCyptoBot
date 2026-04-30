def match(demand, supply):
    supply.sort(key=lambda s: s["price"])
    return supply[0]
