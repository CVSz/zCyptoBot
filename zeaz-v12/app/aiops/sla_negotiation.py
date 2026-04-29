class SLANegotiator:
    def negotiate(self, tenant_req, system_state):
        offer = {}

        if system_state["load"] > 0.8:
            offer["latency"] = tenant_req["latency"] * 1.2
        else:
            offer["latency"] = tenant_req["latency"]

        offer["price"] = tenant_req["cost"] * (1 + system_state["load"])
        return offer
