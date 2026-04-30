def allow(identity, attestation):
    if identity.get("tenant") != "trusted":
        return False
    if attestation.get("region") != "eu":
        return False
    if not attestation.get("secure"):
        return False
    return True
