from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user
from app.limits.quotas import Quota
from app.limits.rate_limit import RateLimiter
from app.metering.usage import Usage
from app.growth.automation import growth_automation

router = APIRouter()
rl = RateLimiter()
qt = Quota()
usage = Usage()


@router.get("/portfolio")
def portfolio(user=Depends(current_user)):
    if not rl.allow():
        raise HTTPException(429, "rate limit")
    if not qt.consume():
        raise HTTPException(402, "quota exceeded")
    usage.inc_req()
    return {"user": user["username"], "tenant": user.get("tenant_id", "public"), "positions": [], "pnl": 0}


@router.post("/onboarding/stage")
def onboarding_stage(user_id: str, stage: str, user=Depends(current_user)):
    event = growth_automation.track_stage(user_id=user_id, stage=stage)
    return {"tracked": event.__dict__}
