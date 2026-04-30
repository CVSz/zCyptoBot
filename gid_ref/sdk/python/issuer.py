def issue(claims: dict, sign_fn):
    """Issue a signed GID token payload."""
    return sign_fn(claims)
