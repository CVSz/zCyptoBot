import os
import subprocess


class Patcher:
    def argocd_sync(self, app: str = "zeaz"):
        subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                f"{os.environ.get('ARGOCD_SERVER')}/api/v1/applications/{app}/sync",
                "-H",
                f"Authorization: Bearer {os.environ.get('ARGO_TOKEN')}",
            ],
            check=False,
        )
