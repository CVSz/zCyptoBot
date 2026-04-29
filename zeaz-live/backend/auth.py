import jwt

SECRET = "SECRET"


def create(user: str, role: str, tenant: str):
    return jwt.encode({"user": user, "role": role, "tenant": tenant}, SECRET, algorithm="HS256")


def verify(token: str) -> dict:
    return jwt.decode(token, SECRET, algorithms=["HS256"])
