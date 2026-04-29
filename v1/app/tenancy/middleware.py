from starlette.middleware.base import BaseHTTPMiddleware

from app.tenancy.context import set_tenant


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        tid = request.headers.get("X-Tenant-ID", "public")
        set_tenant(tid)
        return await call_next(request)
