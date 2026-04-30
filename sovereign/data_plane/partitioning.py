def partition_key(tenant_id: str, region: str) -> str:
    # hard-partition by tenant+region to avoid cross-tenant leakage
    if not tenant_id or not region:
        raise ValueError("invalid partition inputs")
    return f"{tenant_id}:{region}"
