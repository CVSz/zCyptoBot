import re

TENANT_RE = re.compile(r"^[a-zA-Z0-9_]+$")


def schema_for(tenant: str) -> str:
    if not TENANT_RE.match(tenant):
        raise ValueError("invalid tenant")
    return f"tenant_{tenant}"


def set_schema(cursor, tenant: str) -> None:
    cursor.execute("SELECT set_config('search_path', %s, false)", (schema_for(tenant),))
