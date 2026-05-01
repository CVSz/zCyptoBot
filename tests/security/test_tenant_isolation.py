from fastapi.testclient import TestClient
from auth import create
from main import app

client = TestClient(app)


def test_requires_auth_header():
    response = client.get("/metrics/tenantA")
    assert response.status_code == 401


def test_tenant_isolation_violation():
    token = create(user="u1", role="user", tenant="tenantA")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/metrics/tenantB", headers=headers)
    assert response.status_code == 403
