from .catalog import CATALOG


def search(q: str):
    return [i for i in CATALOG if q.lower() in i["type"].lower()]
