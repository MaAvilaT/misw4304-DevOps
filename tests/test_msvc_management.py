import pytest
from flask import Flask

from msvc_email_blacklists.src.blueprints.msvc_management import management_blueprint, token_required
from msvc_email_blacklists.src.services.authentication_service import AuthenticationService


# Mock the AuthenticationService for testing
class MockAuthenticationService:
    @staticmethod
    def is_valid_jwt(jwt):
        return jwt == "valid_token"


# Apply the mock
AuthenticationService.is_valid_jwt = MockAuthenticationService.is_valid_jwt


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(management_blueprint)
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'pong'


def test_token_required_decorator(client):
    @token_required
    def protected_route():
        return 'protected', 200

    app = Flask(__name__)
    app.add_url_rule('/protected', 'protected', protected_route)
    with app.test_client() as client:
        # Test with invalid token
        response = client.get('/protected', headers={'Authorization': 'invalid_token'})
        assert response.status_code == 401
        assert response.json['message'] == 'Unauthorized'

        # Test with valid token
        response = client.get('/protected', headers={'Authorization': 'valid_token'})
        assert response.status_code == 200
        assert response.data == b'protected'
