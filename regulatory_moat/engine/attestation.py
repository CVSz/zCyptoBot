def generate(summary: dict) -> dict:
    """
    Produces attestations consumable by auditors/partners.
    """
    required = {"controls_passed", "scope", "period"}
    if not required.issubset(summary):
        raise ValueError("invalid attestation")
    return {
        "attestation": "COMPLIANT" if summary["controls_passed"] else "NON_COMPLIANT",
        "scope": summary["scope"],
        "period": summary["period"],
    }
