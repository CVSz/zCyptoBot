from ai.fraud.graph_model import anomaly_score


def is_fraud(tx):
    score = anomaly_score(tx["user"])
    return score > 10
