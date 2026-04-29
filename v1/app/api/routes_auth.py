from fastapi import APIRouter

from app.auth.jwt import sign

router = APIRouter()


@router.post("/login")
def login(username: str, role: str, tenant_id: str = "public"):
    return {"access_token": sign({"username": username, "role": role, "tenant_id": tenant_id})}
