from starlette.exceptions import HTTPException
from starlette.requests import Request


def gid_middleware(verify_fn):
    async def middleware(request: Request, call_next):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            claims = verify_fn(token)
            request.state.claims = claims
        except Exception as exc:
            raise HTTPException(status_code=401, detail="unauthorized") from exc
        return await call_next(request)

    return middleware
