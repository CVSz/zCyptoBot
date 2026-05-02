

def run(cases, verify_fn):
    results = []
    for c in cases:
        try:
            verify_fn(c["token"])
            results.append((c["name"], "pass"))
        except Exception:
            results.append((c["name"], "fail"))
    return results
