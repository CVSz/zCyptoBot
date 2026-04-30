REGISTRY = {}


def register(id, att):
    REGISTRY[id] = att


def get(id):
    return REGISTRY.get(id)
