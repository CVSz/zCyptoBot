def payoff(actions):
    """
    Simple payoff heuristic.
    """
    score = 0

    if "compliance" in actions["platform"]:
        score += 3
    if "multi_cloud" in actions["platform"]:
        score += 2
    if "price_cut" in actions["hyperscaler"]:
        score -= 1  # margin pressure
    if "standardize" in actions["regulator"]:
        score += 2  # favors neutral platform

    return score
