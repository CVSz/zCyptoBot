from math import exp, log

PRIORS = {
    "cpu_saturation": 0.25,
    "memory_pressure": 0.2,
    "kafka_backlog": 0.25,
    "bad_deploy": 0.2,
    "network_issue": 0.1,
}

LIKELIHOODS = {
    "latency_high": {
        "cpu_saturation": 0.7,
        "memory_pressure": 0.5,
        "kafka_backlog": 0.6,
        "bad_deploy": 0.6,
        "network_issue": 0.4,
    },
    "error_high": {
        "cpu_saturation": 0.4,
        "memory_pressure": 0.6,
        "kafka_backlog": 0.5,
        "bad_deploy": 0.8,
        "network_issue": 0.5,
    },
    "lag_high": {
        "cpu_saturation": 0.3,
        "memory_pressure": 0.4,
        "kafka_backlog": 0.9,
        "bad_deploy": 0.4,
        "network_issue": 0.6,
    },
}


class BayesianRCA:
    def infer(self, evidence: dict) -> list[tuple[str, float]]:
        scores = {}
        for cause, prior in PRIORS.items():
            logp = log(prior)
            for signal, present in evidence.items():
                likelihood = LIKELIHOODS[signal].get(cause, 0.5)
                logp += log(likelihood if present else (1 - likelihood))
            scores[cause] = logp

        max_logp = max(scores.values())
        weighted = {cause: exp(value - max_logp) for cause, value in scores.items()}
        total = sum(weighted.values())
        return sorted(
            [(cause, value / total) for cause, value in weighted.items()],
            key=lambda item: item[1],
            reverse=True,
        )
