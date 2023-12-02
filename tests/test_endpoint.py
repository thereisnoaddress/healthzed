from fastapi.testclient import TestClient
from healthzed.endpoint import app
import requests
import json

client = TestClient(app)


def test_check_health():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
