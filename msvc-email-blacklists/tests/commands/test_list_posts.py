import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.commands.list_posts import ListPosts
from src.models.models import Post
from src.errors.errors import BadRequestError
import uuid
import datetime

class TestListPosts(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.posts = [
            Post(id=1, userId="user1", routeId="route1", expireAt="2023-12-31", createdAt="2023-01-01"),
            Post(id=2, userId="user2", routeId="route2", expireAt="2023-12-31", createdAt="2023-01-02")
        ]

    def tearDown(self):
        self.app_context.pop()

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_with_posts(self, mock_open_session):
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.all.return_value = self.posts
        list_posts = ListPosts(expire=None, route=None, owner=None)

        mock_response = MagicMock()
        mock_response.json = [post.__dict__ for post in self.posts]
        mock_response.status_code = 200
        list_posts.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = list_posts.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.json), 2)

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_no_posts(self, mock_open_session):
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.all.return_value = []
        list_posts = ListPosts(expire=None, route=None, owner=None)

        mock_response = MagicMock()
        mock_response.json = []
        mock_response.status_code = 200
        list_posts.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = list_posts.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.json), 0)

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_with_filter(self, mock_open_session):
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.filter.return_value.all.return_value = [self.posts[0]]
        list_posts = ListPosts(expire=None, route="route1", owner=None)

        mock_response = MagicMock()
        mock_response.json = [self.posts[0].__dict__]
        mock_response.status_code = 200
        list_posts.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = list_posts.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['id'], 1)

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_invalid_route_filter(self, mock_open_session):
        list_posts = ListPosts(expire=None, route="invalid-uuid", owner=None)
        with self.assertRaises(BadRequestError):
            list_posts.execute()

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_invalid_owner_filter(self, mock_open_session):
        list_posts = ListPosts(expire=None, route=None, owner="invalid-uuid")
        with self.assertRaises(BadRequestError):
            list_posts.execute()

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_valid_route_filter(self, mock_open_session):
        valid_uuid = str(uuid.uuid4())
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.filter.return_value.all.return_value = [self.posts[0]]
        list_posts = ListPosts(expire=None, route=valid_uuid, owner=None)

        mock_response = MagicMock()
        mock_response.json = [self.posts[0].__dict__]
        mock_response.status_code = 200
        list_posts.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = list_posts.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.json), 1)

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_valid_owner_filter(self, mock_open_session):
        valid_uuid = str(uuid.uuid4())
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.filter.return_value.all.return_value = [self.posts[0]]
        list_posts = ListPosts(expire=None, route=None, owner=valid_uuid)

        mock_response = MagicMock()
        mock_response.json = [self.posts[0].__dict__]
        mock_response.status_code = 200
        list_posts.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = list_posts.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.json), 1)

    @patch('src.commands.list_posts.open_session')
    def test_list_posts_with_expire_filter(self, mock_open_session):
        session = mock_open_session.return_value.__enter__.return_value
        session.query.return_value.filter.return_value.all.return_value = [self.posts[0]]
        list_posts = ListPosts(expire=True, route=None, owner=None)

        mock_response = MagicMock()
        mock_response.json = [self.posts[0].__dict__]
        mock_response.status_code = 200
        list_posts.execute = MagicMock(return_value=(mock_response, 200))

        response, status_code = list_posts.execute()
        self.assertEqual(status_code, 200)
        self.assertEqual(len(response.json), 1)

if __name__ == '__main__':
    unittest.main()