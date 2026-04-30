def attest(workload: dict):
    if not workload.get("region"):
        raise ValueError("missing region")
    return {
        "region": workload["region"],
        "secure": workload.get("secure", False),
        "runtime": workload.get("runtime", "unknown"),
    }
