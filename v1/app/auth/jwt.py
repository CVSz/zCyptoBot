import time

import jwt

SECRET = "CHANGE_ME_STRONG"


def sign(payload: dict, ttl: int = 3600) -> str:
    data = dict(payload)
    data["exp"] = int(time.time()) + ttl
    return jwt.encode(data, SECRET, algorithm="HS256")


def verify(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=["HS256"])
