import pytest
from flask import Flask, json
from blueprints.msvc_email_blacklists import email_blacklists_blueprint
from services.email_blacklisting_service import BlacklistedEmailService


# Mock the BlacklistedEmailService for testing
class MockBlacklistedEmailService:
    @staticmethod
    def is_blacklisted(email):
        if email == "blacklisted@example.com":
            return {"msg": "email already blacklisted"}, 409
        return {"msg": "email not blacklisted"}, 200

    @staticmethod
    def create_email_blacklisting(data):
        if data["email"] == "blacklisted@example.com":
            return {"msg": "email already blacklisted"}, 409
        return {"msg": "email blacklisted successfully"}, 201


# Apply the mock
BlacklistedEmailService.is_blacklisted = MockBlacklistedEmailService.is_blacklisted
BlacklistedEmailService.create_email_blacklisting = MockBlacklistedEmailService.create_email_blacklisting


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(email_blacklists_blueprint)
    with app.test_client() as client:
        yield client


def test_create_email_blacklisting_missing_data(client):
    data = {
        "email": "test@example.com",
        "appUuid": "12345"
    }
    response = client.post('/blacklists', data=json.dumps(data), content_type='application/json', headers={'Authorization': 'valid_token'})
    assert response.status_code == 400
    assert b'bad request' in response.data


def test_create_email_blacklisting_valid_request(client):
    data = {
        "email": "test@example.com",
        "appUuid": "12345",
        "blockedReason": "spam"
    }
    response = client.post('/blacklists', data=json.dumps(data), content_type='application/json', headers={'Authorization': 'valid_token'})
    assert response.status_code == 201
    assert b'email blacklisted successfully' in response.data


def test_create_email_blacklisting_already_blacklisted(client):
    data = {
        "email": "blacklisted@example.com",
        "appUuid": "12345",
        "blockedReason": "spam"
    }
    response = client.post('/blacklists', data=json.dumps(data), content_type='application/json', headers={'Authorization': 'valid_token'})
    assert response.status_code == 409
    assert b'email already blacklisted' in response.data


def test_is_blacklisted_missing_email(client):
    response = client.get('/blacklists/', headers={'Authorization': 'valid_token'})
    assert response.status_code == 404  # Flask will return 404 for missing URL parameter


def test_is_blacklisted_valid_request(client):
    response = client.get('/blacklists/test@example.com', headers={'Authorization': 'valid_token'})
    assert response.status_code == 200
    assert b'email not blacklisted' in response.data


def test_is_blacklisted_already_blacklisted(client):
    response = client.get('/blacklists/blacklisted@example.com', headers={'Authorization': 'valid_token'})
    assert response.status_code == 409
    assert b'email already blacklisted' in response.data