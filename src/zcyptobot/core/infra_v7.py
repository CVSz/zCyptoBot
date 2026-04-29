from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class V7InfraConfig:
    environment: str = "prod"
    region: str = "us-east-1"
    k8s_namespace: str = "trading"
    rl_learner_replicas: int = 3
    rl_actor_replicas: int = 24
    redis_replicas: int = 3


class InfraBlueprintV7:
    """v7: full K8s + Terraform infrastructure blueprint."""

    def terraform_vars(self, cfg: V7InfraConfig) -> dict[str, str | int]:
        return {
            "environment": cfg.environment,
            "region": cfg.region,
            "namespace": cfg.k8s_namespace,
            "rl_node_group_size": cfg.rl_learner_replicas + (cfg.rl_actor_replicas // 6),
            "redis_replicas": cfg.redis_replicas,
        }

    def helm_values(self, cfg: V7InfraConfig) -> dict[str, str | int | dict[str, int]]:
        return {
            "namespace": cfg.k8s_namespace,
            "replicaCount": 3,
            "rl": {
                "learners": cfg.rl_learner_replicas,
                "actors": cfg.rl_actor_replicas,
            },
            "redis": {
                "replicas": cfg.redis_replicas,
            },
        }
