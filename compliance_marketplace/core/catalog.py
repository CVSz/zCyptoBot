CATALOG = []


def add(item):
    required = {"id", "type", "price", "partner"}
    if not required.issubset(item):
        raise ValueError("invalid item")
    CATALOG.append(item)
    return item
