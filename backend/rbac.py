ROLES = {
    "viewer": 1,
    "operator": 2,
    "admin": 3,
}


def authorize(user_role: str, required: str) -> None:
    if user_role not in ROLES or required not in ROLES:
        raise PermissionError("forbidden")
    if ROLES[user_role] < ROLES[required]:
        raise PermissionError("forbidden")
