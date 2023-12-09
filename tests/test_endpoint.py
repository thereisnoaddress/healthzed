import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from healthzed.endpoint import app
from healthzed.protocol import PingRequest, PingResponse


class TestEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.request_data = {"message": "Hello World!", "phone_number": "+1234567890"}

    def test_check_health(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

    def test_send_ping(self):
        # WHEN
        response = self.client.post("/send_ping", json=self.request_data)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"status_code": 200, "message": "Ping sent successfully!"}
        )

    @patch("healthzed.notification_service.NotificationService.process_sns_endpoint")
    def test_sns_endpoint(self, mock_process_sns_endpoint):
        # GIVEN
        mock_process_sns_endpoint.return_value = {"status": "ok"}

        # WHEN
        response = self.client.post("/sns_endpoint", json={})

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @patch(
        "healthzed.notification_service.NotificationService.send_pinpoint_sms_notification"
    )
    @patch("healthzed.notification_service.NotificationService.check_received_messages")
    def test_send_and_wait(
        self, mock_check_received_messages, mock_send_pinpoint_sms_notification
    ):
        # GIVEN
        mock_check_received_messages.return_value = "Reply message"

        # WHEN
        response = self.client.post("/send_and_wait", json=self.request_data)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "Message received",
                "number": "+1234567890",
                "message": "Reply message",
            },
        )

    @patch(
        "healthzed.notification_service.NotificationService.send_pinpoint_sms_notification"
    )
    @patch("healthzed.notification_service.NotificationService.check_received_messages")
    def test_send_and_wait_timeout(
        self, mock_check_received_messages, mock_send_pinpoint_sms_notification
    ):
        # GIVEN
        # for mock timeout
        mock_check_received_messages.side_effect = TimeoutError

        # WHEN
        # THEN
        with self.assertRaises(TimeoutError):
            response = self.client.post("/send_and_wait", json=self.request_data)
