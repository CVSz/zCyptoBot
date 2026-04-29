def conversion_rate(step_users: int, next_step_users: int) -> float:
    return next_step_users / max(step_users, 1)


def optimize(step: float) -> str | None:
    if step < 0.3:
        return "improve UX / incentives"
    return None
