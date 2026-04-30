from typing import Dict, List


class PolicyEngine:
    """
    Evaluates whether a resource meets control requirements.
    """

    def evaluate(self, resource: Dict, controls: List[Dict]) -> Dict:
        results = []
        for c in controls:
            if c["id"] == "EN-01":
                ok = resource.get("encryption") in {"AES256", "AES-256", "AES256-GCM"}
            elif c["id"] == "AC-01":
                ok = resource.get("auth") in {"mTLS", "OIDC", "SSO"}
            else:
                ok = True
            results.append({"control": c["id"], "pass": bool(ok)})
        return {"results": results, "passed": all(r["pass"] for r in results)}
