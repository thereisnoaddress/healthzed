from fastapi.testclient import TestClient
from healthzed.endpoint import app

client = TestClient(app)


def test_check_health():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() is True
