from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RLClusterConfig:
    learner_replicas: int = 2
    actor_replicas: int = 16
    replay_buffer_shards: int = 4
    gpu_per_learner: int = 1


class RLTrainingPlanner:
    """Capacity planner for distributed RL workloads."""

    def resources(self, cfg: RLClusterConfig) -> dict[str, int]:
        return {
            "learner_pods": cfg.learner_replicas,
            "actor_pods": cfg.actor_replicas,
            "replay_shards": cfg.replay_buffer_shards,
            "total_gpus": cfg.learner_replicas * cfg.gpu_per_learner,
        }
