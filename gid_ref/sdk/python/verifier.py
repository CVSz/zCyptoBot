def verify(token: str, verify_fn):
    """Verify and decode a GID token."""
    return verify_fn(token)
