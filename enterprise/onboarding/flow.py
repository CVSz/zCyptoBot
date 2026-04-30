"""Enterprise onboarding stage evaluation."""


def stage(user):
    """Return the customer's onboarding stage."""
    if not user.get("contract_signed"):
        return "contract"
    if not user.get("integration_done"):
        return "integration"
    if not user.get("first_workload"):
        return "activation"
    return "active"
