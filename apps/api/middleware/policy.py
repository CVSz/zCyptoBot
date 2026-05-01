from fastapi import HTTPException, Request

from infra.policy.opa_client import check_cost, check_tenant


async def policy_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    payload = {}

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    if not check_tenant(
        {
            "principal": {"tenant_id": tenant_id, "roles": ["user"]},
            "resource": {"tenant_id": payload.get("tenant_id", tenant_id)},
            "action": request.method.lower(),
        }
    ):
        raise HTTPException(403, "tenant policy denied")

    if not check_cost(
        {
            "tenant_id": tenant_id,
            "request_cost": payload.get("cost", 0.0),
            "budget": 100.0,
            "used": 0.0,
        }
    ):
        raise HTTPException(402, "budget exceeded")

    return await call_next(request)
