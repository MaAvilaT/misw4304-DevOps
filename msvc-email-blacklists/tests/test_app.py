import unittest

from .app import app
from flask import json


class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()

    def test_health_route(self):
        """Test the /health route"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'pong')

    def test_create_email_blacklisting_created(self):
        """Test successful creation of email blacklisting with status 201"""
        data = {
            "email": "unique@example.com",
            "appUuid": "12345",
            "blockedReason": "spam"
        }
        response = self.client.post('/blacklists', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Expecting creation success

    def test_create_email_blacklisting_conflict(self):
        """Test conflict error if email already blacklisted with status 409"""
        data = {
            "email": "existing@example.com",  # Assume this email is already blacklisted
            "appUuid": "12345",
            "blockedReason": "spam"
        }
        response = self.client.post('/blacklists', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)  # Expecting conflict

    def test_create_email_blacklisting_bad_request(self):
        """Test bad request error when missing data for email blacklisting with status 400"""
        data = {
            "email": "test@example.com",
            "appUuid": "12345"
        }
        response = self.client.post('/blacklists', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'bad request', response.data)

    def test_is_blacklisted_success(self):
        """Test successful check if email is blacklisted"""
        email = "test@example.com"
        response = self.client.get(f'/blacklists/{email}')
        self.assertIn(response.status_code, [200, 404])

    def test_is_blacklisted_bad_request(self):
        """Test bad request error when email is missing in blacklist check"""
        response = self.client.get('/blacklists/')
        self.assertEqual(response.status_code, 404)  # As per route requirement


if __name__ == "__main__":
    unittest.main()
