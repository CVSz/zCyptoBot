def validate_identity_policy(policy: dict) -> bool:
    mfa = policy.get("mfa_required", False)
    session_hours = policy.get("max_session_hours", 24)
    return bool(mfa) and session_hours <= 12
