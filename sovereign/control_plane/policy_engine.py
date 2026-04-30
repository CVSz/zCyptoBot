class PolicyEngine:
    """
    Deny any cross-border processing of PII by default.
    """

    def allow(self, src_region: str, dst_region: str, data_class: str) -> bool:
        if data_class == "PII" and src_region.startswith("eu") and not dst_region.startswith("eu"):
            return False
        return True
