from dataclasses import dataclass


@dataclass
class Metrics:
    arr: float
    growth: float
    gross_margin: float
    burn: float
    cac: float
    arpu: float
    retention: float


def project(m: Metrics, years: int = 5):
    arr = m.arr
    results = []
    for y in range(1, years + 1):
        arr *= (1 + m.growth)
        profit = arr * m.gross_margin
        results.append({"year": y, "arr": arr, "profit": profit, "burn": m.burn})
    return results


def dcf(cashflows, discount: float = 0.12):
    return sum(cf / (1 + discount) ** i for i, cf in enumerate(cashflows, 1))


def unit_economics(m: Metrics):
    ltv = m.arpu * m.retention
    return {"LTV": ltv, "CAC": m.cac, "LTV/CAC": ltv / m.cac if m.cac else 0}
