import subprocess
from pathlib import Path


class Agent:
    def __init__(self, role):
        self.role = role

    def generate_code(self, task):
        return f"# {self.role} generated code for {task}\n"

    def deploy(self, deployment_manifest="deployment.yaml"):
        subprocess.run(["kubectl", "apply", "-f", deployment_manifest], check=True)


class AIOrg:
    def __init__(self, output_path="generated.py"):
        self.output_path = Path(output_path)
        self.agents = {
            "product": Agent("product"),
            "infra": Agent("infra"),
            "growth": Agent("growth"),
        }

    def execute(self, task, deployment_manifest="deployment.yaml"):
        code = self.agents["product"].generate_code(task)
        self.output_path.write_text(code, encoding="utf-8")
        self.agents["infra"].deploy(deployment_manifest)
        return code
