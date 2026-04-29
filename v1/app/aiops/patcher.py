from pathlib import Path
import subprocess

import yaml


def apply_patch(repo_path: str, policy_rel_path: str, policy: dict, message: str = "auto policy update"):
    full_path = Path(repo_path) / policy_rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with full_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(policy, handle, sort_keys=False)

    subprocess.run(["git", "add", str(full_path)], cwd=repo_path, check=False)
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=False)
    return full_path
