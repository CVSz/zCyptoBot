HISTORY = []


def record(result):
    HISTORY.append(result)


def adjust():
    """
    Tune weights based on win/loss history.
    """
    wins = [h for h in HISTORY if h["win"]]
    return len(wins) / max(len(HISTORY), 1)
