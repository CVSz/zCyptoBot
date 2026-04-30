def export_user(data, user_id: str):
    return [r for r in data if r.get("user_id") == user_id]


def delete_user(data, user_id: str):
    return [r for r in data if r.get("user_id") != user_id]
