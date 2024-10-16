import unittest
from unittest.mock import patch
from flask import Flask, jsonify
from src.blueprints.post_management import posts_blueprint
from src.errors.errors import ApiError, ExpireAtError, BadRequestError

class TestCreatePost(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(posts_blueprint)
        self.client = self.app.test_client()
        @self.app.errorhandler(ApiError)
        def handle_exception(err):
            response = {
                "msg": err.description
            }
            return jsonify(response), err.code

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('{"message": "Post created successfully"}', 201)
        payload = {'routeId': 'route123', 'expireAt': '2023-12-31T23:59:59Z'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_invalid_expireAt(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = ExpireAtError("Invalid expireAt date")
        payload = {'routeId': 'route123', 'expireAt': '2020-01-01T00:00:00Z'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 412)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_database_error(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = BadRequestError("Database error")
        payload = {'routeId': 'route123', 'expireAt': '2023-12-31T23:59:59Z'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_missing_fields(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = BadRequestError
        payload = {'expireAt': '2023-12-31T23:59:59Z'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_invalid_payload(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        payload = {'invalidField': 'invalidValue'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()