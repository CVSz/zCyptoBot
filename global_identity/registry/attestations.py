REG = {}


def put(sub: str, att: dict):
    REG[sub] = att


def get(sub: str):
    return REG.get(sub)
