# path: dora/reporting/incident_report.py
def report(incident):
    return {
        "id": incident["id"],
        "impact": incident["impact"],
        "rto": incident["rto"],
        "rpo": incident["rpo"],
        "actions": incident["actions"]
    }
