#!/usr/bin/env bash
set -e

python - <<'PY'
from agents.evolver import Evolver
from agents.validator import Validator
from agents.guardrails import Guardrails
from agents.patcher import Patcher

e = Evolver()
v = Validator()
g = Guardrails()
p = Patcher()

policy = e.propose_policy({"latency_threshold": 180})
import pathlib
import yaml

pathlib.Path("devops/policies/policy.yaml").write_text(yaml.dump(policy))

ok, meta = v.validate()

if ok and g.ips_dr_gate(meta["sim_score"]):
    e.commit_patch(
        [{"file": "devops/policies/policy.yaml", "content": open("devops/policies/policy.yaml").read()}],
        "auto: policy update",
    )
    p.argocd_sync("zeaz")
    print("PROMOTED")
else:
    print("REJECTED", ok, meta)
PY
