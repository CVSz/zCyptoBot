import os
from typing import Any

import jwt
from fastapi import HTTPException

PUBLIC_KEY = os.getenv("OIDC_PUBLIC_KEY", "")
EXPECTED_AUDIENCE = os.getenv("OIDC_AUDIENCE")
EXPECTED_ISSUER = os.getenv("OIDC_ISSUER")


def verify(token: str) -> dict[str, Any]:
    if not PUBLIC_KEY:
        raise HTTPException(status_code=500, detail="OIDC_PUBLIC_KEY missing")
    try:
        return jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
            options={"verify_aud": EXPECTED_AUDIENCE is not None},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="invalid token") from exc
