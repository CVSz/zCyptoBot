from pathlib import Path
from typing import Dict

try:
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    yaml = None


def _coerce_scalar(value: str):
    text = value.strip()
    if text.lower() in {"true", "false"}:
        return text.lower() == "true"
    for caster in (int, float):
        try:
            return caster(text)
        except ValueError:
            continue
    return text


def _simple_yaml_load(raw: str) -> dict:
    root: dict = {}
    current = root
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, _, value = line.strip().partition(":")
        if indent == 0:
            if value.strip():
                root[key] = _coerce_scalar(value)
                current = root
            else:
                root[key] = {}
                current = root[key]
        elif indent >= 2:
            current[key] = _coerce_scalar(value)
    return root


class RewriteEngine:
    def propose_patch(self, policy_path: str, updates: Dict[str, float]) -> dict:
        raw = Path(policy_path).read_text(encoding="utf-8")
        if yaml is not None:
            policy = yaml.safe_load(raw) or {}
        else:
            policy = _simple_yaml_load(raw)

        rules = policy.setdefault("rules", {})
        for key, value in updates.items():
            rules[key] = value
        return policy
