import subprocess


class CloudScaler:
    def __init__(self, max_replicas: int = 8):
        self.max_replicas = max_replicas

    def scale_cluster(self, cluster: str, replicas: int):
        bounded = max(1, min(self.max_replicas, replicas))
        return subprocess.run(
            [
                "kubectl",
                "--context",
                cluster,
                "scale",
                "deploy/zeaz-api",
                f"--replicas={bounded}",
            ],
            check=False,
        )

    def shift_traffic(self, from_region: str, to_region: str, pct: int = 20):
        patch = (
            '{"spec":{"rules":['
            f'{{"host":"{from_region}","weight":{100 - pct}}},'
            f'{{"host":"{to_region}","weight":{pct}}}'
            "]}}"
        )
        return subprocess.run(
            ["kubectl", "patch", "ingress", "zeaz", "--type=merge", "-p", patch],
            check=False,
        )
