from typing import Any, Dict, Iterable


class Replay:
    """Deterministic replay utility for forensic reconstruction."""

    def run(self, logs: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        state: Dict[str, Any] = {}
        for entry in logs:
            state.update(entry["event"])
        return state
