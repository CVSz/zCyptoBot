from .base import Adapter


class BankAdapter(Adapter):
    def charge(self, account: str, amount: float):
        return {"ok": True, "type": "bank_charge", "account": account, "amount": amount}

    def payout(self, account: str, amount: float):
        return {"ok": True, "type": "bank_payout", "account": account, "amount": amount}
