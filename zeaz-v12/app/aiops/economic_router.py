from app.aiops.carbon import CarbonModel
from app.aiops.pricing_rt import PricingEngine
from app.aiops.sla_negotiation import SLANegotiator


class EconomicRouter:
    def __init__(self):
        self.carbon = CarbonModel()
        self.pricing = PricingEngine()
        self.sla = SLANegotiator()

    def route(self, state, tenant_req):
        region = self.carbon.best_region(state["regions"])
        carbon_score = self.carbon.score(region, state["load"])

        price = self.pricing.price(state["load"], state["demand"], carbon_score)
        sla_offer = self.sla.negotiate(tenant_req, state)

        return {"region": region, "price": price, "sla": sla_offer}
