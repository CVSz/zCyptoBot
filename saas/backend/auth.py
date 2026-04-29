import os
from datetime import datetime, timedelta, timezone

import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ISSUER = os.getenv("JWT_ISSUER", "zeaz-api")


def create_token(user: dict) -> str:
    claims = {
        **user,
        "iss": JWT_ISSUER,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=2),
    }
    return jwt.encode(claims, JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer=JWT_ISSUER)
