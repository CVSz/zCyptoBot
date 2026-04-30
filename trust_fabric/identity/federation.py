TRUSTED_ISSUERS = set()


def add_issuer(issuer: str):
    TRUSTED_ISSUERS.add(issuer)


def is_trusted(issuer: str) -> bool:
    return issuer in TRUSTED_ISSUERS
