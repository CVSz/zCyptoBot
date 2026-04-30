from dataclasses import dataclass


@dataclass(frozen=True)
class TenantIdentity:
    tenant_id: str
    tenant_region: str
    tier: str = "standard"


def assert_eu_scope(identity: TenantIdentity) -> None:
    if not identity.tenant_id or not identity.tenant_region:
        raise ValueError("missing tenant identity")
    if identity.tenant_region != "EU":
        raise PermissionError("tenant is outside EU sovereign boundary")
