import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET = os.getenv("JWT_SECRET", "change-me")
security = HTTPBearer()


def create_token(user: str, tenant: str, expires_minutes: int = 60) -> str:
    payload = {
        "user": user,
        "tenant": tenant,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(401, "invalid token") from exc


def verify_credentials(credentials: HTTPAuthorizationCredentials) -> dict:
    return verify(credentials.credentials)
