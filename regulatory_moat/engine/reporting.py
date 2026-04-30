def report(run_state):
    total = len(run_state)
    passed = sum(1 for r in run_state if r["result"]["passed"])
    return {
        "controls_total": total,
        "controls_passed": passed,
        "compliance_rate": passed / max(total, 1),
    }
