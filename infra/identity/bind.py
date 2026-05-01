"""Bind successful attestation evidence to a SPIFFE identity."""


def issue_spiffe_id(attestation_ok: bool, namespace: str = "secure", service_account: str = "workload") -> str:
    if not attestation_ok:
        raise ValueError("untrusted workload")

    return f"spiffe://zypto.global/ns/{namespace}/sa/{service_account}"
