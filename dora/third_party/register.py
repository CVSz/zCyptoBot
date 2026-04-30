# path: dora/third_party/register.py

REGISTRY = []

def add(name, service, criticality):
    REGISTRY.append({
        "name": name,
        "service": service,
        "criticality": criticality
    })
