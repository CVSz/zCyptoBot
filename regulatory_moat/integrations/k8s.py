def validate_pod(pod_spec: dict) -> bool:
    # enforce no public exposure + require mTLS sidecar label
    if pod_spec.get("public", False):
        return False
    return pod_spec.get("mtls", False) is True
