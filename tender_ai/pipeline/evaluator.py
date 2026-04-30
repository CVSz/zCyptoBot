from tender_ai.optimization.scoring_model import score


def evaluate(proposal_metrics: dict) -> float:
    return score(proposal_metrics)
