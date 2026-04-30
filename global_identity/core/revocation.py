REVOKED = set()


def revoke(jti: str):
    REVOKED.add(jti)


def is_revoked(jti: str) -> bool:
    return jti in REVOKED
