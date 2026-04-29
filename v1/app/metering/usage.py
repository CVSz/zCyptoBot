from collections import defaultdict

from app.tenancy.context import get_tenant


class Usage:
    def __init__(self):
        self.req = defaultdict(int)
        self.trades = defaultdict(int)

    def inc_req(self):
        self.req[get_tenant()] += 1

    def inc_trade(self):
        self.trades[get_tenant()] += 1
