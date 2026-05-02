import time

import importlib

_pyjwt = importlib.import_module("jwt")

SECRET = "CHANGE_ME_STRONG"


def sign(payload: dict, ttl: int = 3600) -> str:
    data = dict(payload)
    data["exp"] = int(time.time()) + ttl
    return _pyjwt.encode(data, SECRET, algorithm="HS256")


def verify(token: str) -> dict:
    return _pyjwt.decode(token, SECRET, algorithms=["HS256"])
