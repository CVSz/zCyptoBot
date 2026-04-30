# path: dora/reporting/kpi.py
def kpi(rto, rpo, incidents):
    return {
        "RTO": rto,
        "RPO": rpo,
        "Incidents": incidents
    }
