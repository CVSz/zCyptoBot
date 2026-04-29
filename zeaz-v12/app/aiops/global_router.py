class GlobalRouter:
    """Simple active-active traffic policy with failover path."""

    def split(self, healthy_regions):
        if len(healthy_regions) <= 1:
            return {healthy_regions[0]: 100} if healthy_regions else {}

        weight = int(100 / len(healthy_regions))
        routing = {region: weight for region in healthy_regions}
        remainder = 100 - sum(routing.values())
        if remainder:
            routing[healthy_regions[0]] += remainder
        return routing

    def failover(self, primary, backup, primary_healthy=True):
        return primary if primary_healthy else backup
