from abc import ABC, abstractmethod


class Adapter(ABC):
    @abstractmethod
    def charge(self, account: str, amount: float):
        raise NotImplementedError

    @abstractmethod
    def payout(self, account: str, amount: float):
        raise NotImplementedError
