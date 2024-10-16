import unittest
from unittest.mock import patch
from flask import Flask, jsonify
from src.blueprints.post_management import posts_blueprint
from src.errors.errors import ApiError, PostNotFoundError, InvalidTokenError

class TestDeletePost(unittest.TestCase):
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
    @patch('src.commands.delete_post.DeletePost.execute')
    def test_delete_post_success(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.return_value = ('{"message": "Post deleted successfully"}', 200)
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.delete('/posts/post1', headers=headers)
        self.assertEqual(response.status_code, 200)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.delete_post.DeletePost.execute')
    def test_delete_post_not_found(self, mock_execute, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        mock_execute.side_effect = PostNotFoundError("Post not found")
        headers = {'Authorization': 'Bearer valid_token'}
        response = self.client.delete('/posts/nonexistent_post', headers=headers)
        self.assertEqual(response.status_code, 404)

    @patch('src.commands.common.Common.verify_token')
    @patch('src.commands.delete_post.DeletePost.execute')
    def test_delete_post_unauthorized(self, mock_execute, mock_verify_token):
        mock_verify_token.side_effect = InvalidTokenError("Invalid token")
        headers = {'Authorization': 'Bearer invalid_token'}
        response = self.client.delete('/posts/post1', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()