# path: dora/third_party/risk_scoring.py

def score(uptime, incidents, geo, lockin):
    """
    Higher is riskier. Defensive guards.
    """
    if not (0 <= uptime <= 1):
        raise ValueError("uptime must be 0..1")
    return (1-uptime)*0.4 + incidents*0.3 + (1 if geo != "EU" else 0)*0.2 + lockin*0.1
