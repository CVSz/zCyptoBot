def tenant_filter(query: str, tenant_id: str) -> str:
    return f"{query} WHERE tenant_id = '{tenant_id}'"
