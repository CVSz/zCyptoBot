def expand_contract(contract):
    contract["value"] *= 1.5
    contract["regions"] = ["global"]
    return contract
