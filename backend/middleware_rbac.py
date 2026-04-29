from fastapi import Request


async def rbac_middleware(request: Request, call_next):
    role = request.headers.get("x-role", "viewer")
    request.state.role = role
    return await call_next(request)
