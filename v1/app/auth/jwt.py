import time

from jwt import decode as jwt_decode, encode as jwt_encode

SECRET = "CHANGE_ME_STRONG"


def sign(payload: dict, ttl: int = 3600) -> str:
    data = dict(payload)
    data["exp"] = int(time.time()) + ttl
    return jwt_encode(data, SECRET, algorithm="HS256")


def verify(token: str) -> dict:
    return jwt_decode(token, SECRET, algorithms=["HS256"])
