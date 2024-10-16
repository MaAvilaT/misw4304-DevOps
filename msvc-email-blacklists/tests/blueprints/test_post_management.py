import unittest
from unittest.mock import patch
from flask import Flask, jsonify
from src.blueprints.post_management import posts_blueprint
from src.errors.errors import ApiError, InvalidTokenError, NoTokenError, BadRequestError, ExpireAtError


class TestPostManagement(unittest.TestCase):
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
    def test_create_post_missing_fields(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = BadRequestError
        payload = {'routeId': 'route123'}  # Missing required fields
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

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
    @patch('src.commands.list_posts.ListPosts.execute')
    def test_get_posts_success(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('[{"id": "post1"}, {"id": "post2"}]', 200)
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.get('/posts', headers=headers)
        self.assertEqual(response.status_code, 200)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.delete_post.DeletePost.execute')
    def test_delete_post_success(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('{"message": "Post deleted successfully"}', 200)
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.delete('/posts/post1', headers=headers)
        self.assertEqual(response.status_code, 200)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.get_post.GetPost.execute')
    def test_get_post_success(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('{"id": "post1", "routeId": "route123"}', 200)
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.get('/posts/post1', headers=headers)
        self.assertEqual(response.status_code, 200)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_invalid_payload(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        payload = {'invalidField': 'invalidValue'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.delete_post.DeletePost.execute')
    def test_delete_post_not_found(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('{"message": "Post not found"}', 404)
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.delete('/posts/nonexistent_post', headers=headers)
        self.assertEqual(response.status_code, 404)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.get_post.GetPost.execute')
    def test_get_post_not_found(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('{"message": "Post not found"}', 404)
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.get('/posts/nonexistent_post', headers=headers)
        self.assertEqual(response.status_code, 404)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_expired_token(self, mock_execute, mock_verify_token):
        mock_verify_token.side_effect = InvalidTokenError("Token expired")
        payload = {'routeId': 'route123', 'expireAt': '2023-12-31T23:59:59Z'}
        headers = {'Authorization': 'Bearer expired_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 401)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_no_token(self, mock_execute, mock_verify_token):
        mock_verify_token.side_effect = NoTokenError("No token provided")
        payload = {'routeId': 'route123', 'expireAt': '2023-12-31T23:59:59Z'}
        response = self.client.post('/posts', json=payload)
        self.assertEqual(response.status_code, 403)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_invalid_routeId(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = BadRequestError("Invalid routeId")
        payload = {'routeId': 'invalid_route', 'expireAt': '2023-12-31T23:59:59Z'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.create_post.CreatePost.execute')
    def test_create_post_invalid_expireAt(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = ExpireAtError("Invalid expireAt date")
        payload = {'routeId': 'route123', 'expireAt': '2020-01-01T00:00:00Z'}
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.post('/posts', json=payload, headers=headers)
        self.assertEqual(response.status_code, 412)

if __name__ == '__main__':
    unittest.main()