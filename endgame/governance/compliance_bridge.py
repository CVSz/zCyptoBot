def validate(proposal):
    """
    Ensure DAO decisions align with external regulation.
    """
    if proposal.get("type") == "data_transfer" and proposal.get("region") != "same":
        return "rejected"
    return "approved"
