CHAIN = []


def append(commit_hash: str):
    prev = CHAIN[-1] if CHAIN else "GENESIS"
    CHAIN.append(f"{prev}:{commit_hash}")
    return CHAIN[-1]


def verify_chain() -> bool:
    for i in range(1, len(CHAIN)):
        if ":" not in CHAIN[i]:
            return False
    return True
