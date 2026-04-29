def check(role: str, required: str) -> bool:
    roles = ["viewer", "operator", "admin"]
    return roles.index(role) >= roles.index(required)
