def ips(logs):
    est = 0.0
    for p_new, p_old, reward in logs:
        if p_old > 0:
            est += (p_new / p_old) * reward
    return est / max(1, len(logs))


def doubly_robust(logs, q_hat):
    est = 0.0
    for x, action, p_new, p_old, reward in logs:
        baseline = q_hat(x, action)
        dr = baseline + (p_new / max(p_old, 1e-6)) * (reward - baseline)
        est += dr
    return est / max(1, len(logs))
