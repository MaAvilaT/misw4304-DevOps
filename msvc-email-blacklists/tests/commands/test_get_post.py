import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.commands.get_post import GetPost
from src.models.models import Post
from src.errors.errors import BadRequestError, PostNotFoundError, InvalidUUIDError
import uuid

class TestGetPost(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.post = Post(id=1, userId="user1", routeId="route1", expireAt="2023-12-31", createdAt="2023-01-01")

    def tearDown(self):
        self.app_context.pop()

    @patch('src.commands.get_post.open_session')
    def test_get_post_by_valid_id(self, mock_open_session):
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.get.return_value = self.post
        get_post = GetPost(post_id=1)

        mock_response = MagicMock()
        mock_response.json = self.post.__dict__
        mock_response.status_code = 200
        get_post.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = get_post.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json['id'], 1)

    @patch('src.commands.get_post.open_session')
    def test_get_post_by_invalid_id(self, mock_open_session):
        invalid_id = "invalid-id"  # Use a string to simulate an invalid ID
        get_post = GetPost(post_id=invalid_id)

        with self.assertRaises(InvalidUUIDError):
            get_post.execute()

    @patch('src.commands.get_post.open_session')
    def test_get_post_by_valid_uuid(self, mock_open_session):
        valid_uuid = str(uuid.uuid4())
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.filter.return_value.first.return_value = self.post
        get_post = GetPost(post_id=valid_uuid)

        mock_response = MagicMock()
        mock_response.json = self.post.__dict__
        mock_response.status_code = 200
        get_post.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = get_post.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json['id'], 1)

    @patch('src.commands.get_post.open_session')
    def test_get_post_by_invalid_uuid(self, mock_open_session):
        invalid_uuid = "invalid-uuid"
        get_post = GetPost(post_id=invalid_uuid)

        with self.assertRaises(InvalidUUIDError):
            get_post.execute()

if __name__ == '__main__':
    unittest.main()