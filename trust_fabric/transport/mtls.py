def enforce(cert: dict) -> bool:
    return cert.get("valid") is True and cert.get("issuer") is not None
