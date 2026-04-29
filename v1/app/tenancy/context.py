import contextvars

tenant_id_ctx = contextvars.ContextVar("tenant_id", default="public")


def set_tenant(tid: str) -> None:
    tenant_id_ctx.set(tid)


def get_tenant() -> str:
    return tenant_id_ctx.get()
