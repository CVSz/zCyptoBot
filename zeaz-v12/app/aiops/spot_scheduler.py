class SpotScheduler:
    """Disruption-aware spot placement policy."""

    def choose_pool(self, workload):
        if workload.get("stateful", False):
            return "on-demand"
        return "spot"

    def can_evict(self, replicas, min_available=1):
        return replicas - 1 >= min_available
