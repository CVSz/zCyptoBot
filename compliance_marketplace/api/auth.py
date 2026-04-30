from fastapi import HTTPException


def authorize(token: dict, tenant_id: str):
    if not token or token.get("tenant") != tenant_id:
        raise HTTPException(status_code=403, detail="forbidden")
    return True
