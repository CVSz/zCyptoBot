TENANTS = {}


def create(tenant_id: str):
    if tenant_id in TENANTS:
        raise ValueError("exists")
    TENANTS[tenant_id] = {"policies": [], "resources": []}
    return TENANTS[tenant_id]
