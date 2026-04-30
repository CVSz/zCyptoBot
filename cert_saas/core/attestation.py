def generate(results: list):
    passed = all(all(v for v in r["res"].values()) for r in results)
    return {
        "status": "COMPLIANT" if passed else "NON_COMPLIANT",
        "controls": len(results),
    }
