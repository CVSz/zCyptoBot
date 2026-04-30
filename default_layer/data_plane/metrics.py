def kpis(reqs, success):
    return {"requests": reqs, "success_rate": success / max(reqs, 1)}
