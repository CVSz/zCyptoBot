def strategy(player, state):
    if player == "hyperscaler":
        return "price_cut + lock_in + ai_bundle"
    if player == "platform":
        return "multi_cloud + compliance + marketplace"
    if player == "regulator":
        return "enforce + standardize"
    return "hold"
