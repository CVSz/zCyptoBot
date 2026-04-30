import base64
import json


def verify(token: str) -> dict:
    try:
        data = json.loads(base64.b64decode(token))
        if "sub" not in data:
            raise ValueError("invalid token")
        return data
    except Exception as exc:
        raise ValueError("verification failed") from exc
