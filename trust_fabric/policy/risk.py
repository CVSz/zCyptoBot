def score(identity: dict, attestation: dict) -> int:
    risk = 0
    if identity.get("tenant") != "trusted":
        risk += 50
    if not attestation.get("secure", False):
        risk += 30
    if attestation.get("region") != "eu":
        risk += 20
    return min(risk, 100)
