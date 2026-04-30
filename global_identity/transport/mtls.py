def enforce(cert: dict) -> bool:
    return cert.get("valid") is True and cert.get("cn") is not None
