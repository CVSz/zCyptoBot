BUDGET = 10000


def check_cost(current):
    if current > BUDGET:
        return "scale_down"
    return "ok"
