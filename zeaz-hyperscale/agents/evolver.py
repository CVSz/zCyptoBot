import pathlib
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[1]
POLICY = REPO / "devops/policies/policy.yaml"


class Evolver:
    def propose_policy(self, updates: dict) -> dict:
        import yaml

        p = yaml.safe_load(POLICY.read_text())
        p.setdefault("rules", {}).update(updates)
        return p

    def propose_code_patch(self, file_path: str, find: str, replace: str) -> dict:
        fp = REPO / file_path
        text = fp.read_text()
        if find not in text:
            raise ValueError("pattern not found")
        new_text = text.replace(find, replace)
        return {"file": file_path, "content": new_text}

    def commit_patch(self, changes: list, message: str):
        for ch in changes:
            fp = REPO / ch["file"]
            fp.write_text(ch["content"])
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
