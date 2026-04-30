def respond(event: str):
    if event == "ddos":
        return ["rate_limit", "autoscale", "edge_filter"]
    if event == "key_leak":
        return ["rotate_keys", "revoke_tokens", "force_reauth"]
    if event == "supply_chain":
        return ["failover_multi_cloud", "degrade_noncritical"]
    if event == "regulatory_ban":
        return ["localize_processing", "block_transfer", "update_contracts"]
    return ["monitor"]
