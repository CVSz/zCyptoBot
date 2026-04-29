TENANTS = {}


def get_tenant_state(tid: str):
    if tid not in TENANTS:
        TENANTS[tid] = {
            "latency": 200,
            "error": 0.02,
            "load": 0.5,
        }
    return TENANTS[tid]
