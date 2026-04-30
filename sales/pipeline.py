PIPELINE = ["lead", "qualified", "demo", "proposal", "closed"]


def next_stage(stage):
    i = PIPELINE.index(stage)
    return PIPELINE[min(i + 1, len(PIPELINE) - 1)]
