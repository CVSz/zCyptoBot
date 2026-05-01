import requests

OPA_URL = "http://opa:8181/v1/data/zypto"


def check_tenant(input_data: dict) -> bool:
    response = requests.post(f"{OPA_URL}/authz/allow", json={"input": input_data}, timeout=2)
    response.raise_for_status()
    return response.json().get("result", False)


def check_cost(input_data: dict) -> bool:
    response = requests.post(f"{OPA_URL}/cost/allow", json={"input": input_data}, timeout=2)
    response.raise_for_status()
    return response.json().get("result", False)
