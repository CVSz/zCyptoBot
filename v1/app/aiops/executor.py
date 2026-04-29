import subprocess


def _sh(cmd: list):
    return subprocess.run(cmd, capture_output=True, text=True)


class Executor:
    def scale_api(self, replicas: int = 3):
        return _sh(["kubectl", "scale", "deploy/zeaz-api", f"--replicas={replicas}"])

    def restart_pods(self):
        return _sh(["kubectl", "rollout", "restart", "deployment", "zeaz-api"])

    def rollback_deploy(self):
        return _sh(["kubectl", "rollout", "undo", "deployment", "zeaz-api"])

    def scale_consumers(self, replicas: int = 3):
        return _sh(["kubectl", "scale", "deploy/zeaz-consumer", f"--replicas={replicas}"])

    def restart_kafka(self):
        return _sh(["kubectl", "delete", "pod", "-l", "app=kafka", "--grace-period=30"])
