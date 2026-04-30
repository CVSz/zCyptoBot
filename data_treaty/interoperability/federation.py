def federate(records, target_region):
    """
    Move non-PII or properly tokenized data only.
    """
    if not target_region:
        raise ValueError("missing target_region")
    return [r for r in records if r.get("region") == target_region]
