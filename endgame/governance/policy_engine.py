def enforce(policy, action):
    if policy == "no_cross_border_pii" and action == "transfer":
        return False
    return True
