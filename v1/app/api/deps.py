from fastapi import Header, HTTPException

from app.auth.jwt import verify
from app.tenancy.context import set_tenant


async def current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "invalid token")
    token = authorization.split()[1]
    user = verify(token)
    if user.get("tenant_id"):
        set_tenant(user["tenant_id"])
    return user
