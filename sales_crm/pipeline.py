from sales_crm.models import DEALS

STAGES = ["lead", "qualified", "demo", "pilot", "closed"]


def advance(deal_id: str):
    for deal in DEALS:
        if deal.id == deal_id:
            index = STAGES.index(deal.stage)
            deal.stage = STAGES[min(index + 1, len(STAGES) - 1)]
            return deal.stage
    return None


def pipeline_value() -> float:
    return sum(deal.value * deal.probability for deal in DEALS)
