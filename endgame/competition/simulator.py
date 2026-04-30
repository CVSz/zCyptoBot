from .strategies import strategy


def step(state):
    actions = {
        "hyperscaler": strategy("hyperscaler", state),
        "platform": strategy("platform", state),
        "regulator": strategy("regulator", state),
    }
    return actions
