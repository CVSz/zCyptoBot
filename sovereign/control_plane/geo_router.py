class GeoRouter:
    """
    Routes requests to EU-only infra when data_class=PII or tenant=EU.
    """

    def route(self, req: dict) -> str:
        if "region" not in req or "data_class" not in req:
            raise ValueError("invalid request")

        if req["data_class"] == "PII" or req.get("tenant_region") == "EU":
            return "eu-central-1"
        return req["region"]
