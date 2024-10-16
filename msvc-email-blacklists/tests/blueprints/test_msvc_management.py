import unittest
from unittest.mock import patch
from src.blueprints.msvc_management import management_blueprint
from flask import Flask, jsonify

from src.errors.errors import ApiError


class TestMsvcManagement(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(management_blueprint)
        self.client = self.app.test_client()
        @self.app.errorhandler(ApiError)
        def handle_exception(err):
            response = {
                "msg": err.description
            }
            return jsonify(response), err.code

    def test_ping_endpoint_returns_200(self):
        response = self.client.get('/posts/ping')
        self.assertEqual(response.status_code, 200)

    def test_reset_endpoint_returns_200(self):
        response = self.client.post('/posts/reset')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()