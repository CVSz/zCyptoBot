def choose_issuer(region: str, issuers: dict):
    """Route to region-appropriate issuer (sovereignty-first)."""
    if not region:
        raise ValueError("missing region")
    return issuers.get(region) or issuers.get("default")
