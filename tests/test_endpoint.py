from fastapi.testclient import TestClient
from healthzed.endpoint import app
import requests
import json

client = TestClient(app)


def test_check_health():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_receive_ping(self):
    # GIVEN
    url = "http://127.0.0.1:8000/receive_ping"
    headers = {"Content-Type": "application/json"}
    data = {
        "Type": "Notification",
        "Message": json.dumps(
            {
                "requestPayload": {
                    "Records": [
                        {
                            "Sns": {
                                "Message": json.dumps(
                                    {
                                        "originationNumber": "+16478611345",
                                        "messageBody": "Hello, world!",
                                    }
                                )
                            }
                        }
                    ]
                }
            }
        ),
    }
    # WHEN
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # THEN
    self.assertEqual(response.status_code, 200)
