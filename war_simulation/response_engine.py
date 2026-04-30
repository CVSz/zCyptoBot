from strategies import choose


def respond(events):
    plan = []
    for e in events:
        move = choose(e)
        plan.append({"event": e, "response": move})
    return plan
