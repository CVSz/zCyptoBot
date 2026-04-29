from fastapi import APIRouter, Depends

from app.api.deps import current_user
from app.auth.rbac import require

router = APIRouter()


@router.post("/strategy/toggle")
def toggle_strategy(enable: bool, user=Depends(current_user)):
    require("admin")(user)
    return {"status": "ok", "enabled": enable}
