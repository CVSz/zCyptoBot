def parse_rfp(text: str):
    """
    Extract key requirements using simple heuristics.
    Replace with LLM + schema extraction in production.
    """
    if not text:
        raise ValueError("empty RFP")

    return {
        "compliance": "GDPR" if "GDPR" in text else None,
        "sla": "99.9%" if "SLA" in text else None,
        "budget": 100000 if "budget" in text.lower() else None,
    }
