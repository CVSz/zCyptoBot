PRICE_REQ = 0.0001
PRICE_TRADE = 0.001


class Billing:
    def invoice(self, usage_req: int, usage_trade: int):
        req = usage_req * PRICE_REQ
        trade = usage_trade * PRICE_TRADE
        return {"request_cost": req, "trade_cost": trade, "total": req + trade}
