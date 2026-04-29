from fastapi import HTTPException


ROLE_ORDER = {"user": 1, "admin": 2, "god": 3}


def require(role_required: str):
    def _check(user: dict) -> bool:
        if ROLE_ORDER.get(user.get("role", ""), 0) < ROLE_ORDER.get(role_required, 0):
            raise HTTPException(403, "forbidden")
        return True

    return _check
