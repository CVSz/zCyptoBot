from fastapi import APIRouter, Depends

from app.aiops.safeguards import Safeguards
from app.api.deps import current_user
from app.auth.rbac import require

router = APIRouter()
safe = Safeguards()


@router.post("/kill")
def kill(on: bool, user=Depends(current_user)):
    require("god")(user)
    safe.ks.set(on)
    return {"kill": safe.ks.is_on()}


@router.post("/limit")
def set_limit(v: int, user=Depends(current_user)):
    require("admin")(user)
    safe.max_actions = v
    return {"max_actions": safe.max_actions}
