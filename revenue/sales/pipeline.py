STAGES = ["lead", "qualified", "demo", "contract", "closed"]


def advance(stage):
    i = STAGES.index(stage)
    return STAGES[min(i + 1, len(STAGES) - 1)]
