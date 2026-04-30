from warfare.response import respond


def step(state):
    events = state.get("events", [])
    actions = [respond(e) for e in events]
    return {"actions": actions}
