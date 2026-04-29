def rank(candidate_scores: list):
    return sorted(candidate_scores, key=lambda x: -x["score"])
