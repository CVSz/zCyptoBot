def choose(counter: str) -> str:
    """
    Deterministic mapping for clarity; production can be policy-driven.
    """
    if counter == "price_cut":
        # do not undercut blindly; bundle value
        return "bundle_pricing + target_high_LTV_segments"
    if counter == "compliance_push":
        return "sovereign_compliance_layer + certifications"
    if counter == "lock_in":
        return "multi_cloud_abstraction + portability_guarantee"
    if counter == "ai_bundle":
        return "model_router + vendor_agnostic_ai"
    return "hold"
