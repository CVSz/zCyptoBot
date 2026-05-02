from functools import lru_cache

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

bearer = HTTPBearer()


@lru_cache
def _jwk_client() -> PyJWKClient:
    return PyJWKClient("https://your-domain/.well-known/jwks.json")


def verify_oidc(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    token = credentials.credentials
    try:
        signing_key = _jwk_client().get_signing_key_from_jwt(token)
        return jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="your-client-id",
            issuer="https://your-domain/",
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc
