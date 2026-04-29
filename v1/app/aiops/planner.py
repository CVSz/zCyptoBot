PRIORITY = {
    "rollback_deploy": 1,
    "scale_api": 2,
    "scale_consumers": 2,
    "restart_kafka": 3,
    "restart_pods": 3,
}


class Planner:
    def plan(self, diagnoses: list):
        actions = set()
        for diagnosis in diagnoses:
            actions.update(diagnosis["actions"])
        return sorted(list(actions), key=lambda action: PRIORITY.get(action, 99))
