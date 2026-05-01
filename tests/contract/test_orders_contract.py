from fastapi.testclient import TestClient
from auth import create
from main import app

client = TestClient(app)


def test_metrics_contract_shape():
    token = create(user="u1", role="user", tenant="tenantA")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/metrics/tenantA", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["tenant"] == "tenantA"
    assert "usage" in body
    assert "state" in body
