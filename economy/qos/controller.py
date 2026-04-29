"""QoS selection and prioritization helpers."""

from economy.credits.ledger import balance


def priority(tenant: str) -> float:
    # higher credits -> higher priority
    return balance(tenant)


def allocate(nodes, tenant: str):
    del tenant
    nodes.sort(key=lambda n: -n["capacity"])
    return nodes[0]
