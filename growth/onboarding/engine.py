def onboarding_stage(user: dict) -> str:
    if not user.get("connected_cluster"):
        return "connect_cluster"
    if not user.get("billing"):
        return "setup_billing"
    return "active"
