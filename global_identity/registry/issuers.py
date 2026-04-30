TRUSTED = set()


def add(iss: str):
    TRUSTED.add(iss)


def is_trusted(iss: str) -> bool:
    return iss in TRUSTED
