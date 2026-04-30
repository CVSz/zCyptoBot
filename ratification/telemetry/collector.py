LOG = []


def record(event):
    LOG.append(event)


def summary():
    return {
        "requests": len(LOG),
        "success": sum(1 for e in LOG if e["ok"]),
    }
