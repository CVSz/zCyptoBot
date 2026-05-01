import json
from pathlib import Path

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
SNAP = Path("tests/contract/openapi_snapshot.json")


def test_openapi_contract():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    current = response.json()

    if not SNAP.exists():
        SNAP.write_text(json.dumps(current, indent=2), encoding="utf-8")
        return

    expected = json.loads(SNAP.read_text(encoding="utf-8"))
    assert current == expected, "OpenAPI changed – review required"
