import unittest
from unittest.mock import patch
from src.commands.common import Common
from src.errors.errors import ApiError, InvalidTokenError, NoTokenError

class TestCommon(unittest.TestCase):
    def setUp(self):
        self.common = Common()

    @patch('src.commands.common.Common.verify_token')
    def test_verify_token_success(self, mock_verify_token):
        mock_verify_token.return_value = ({'id': 'user123'}, 200)
        result, status_code = self.common.verify_token('valid_token')
        self.assertEqual(status_code, 200)

    @patch('src.commands.common.Common.verify_token')
    def test_verify_token_invalid(self, mock_verify_token):
        mock_verify_token.side_effect = InvalidTokenError
        with self.assertRaises(InvalidTokenError):
            self.common.verify_token('invalid_token')

    @patch('src.commands.common.Common.verify_token')
    def test_verify_token_missing(self, mock_verify_token):
        mock_verify_token.side_effect = NoTokenError
        with self.assertRaises(NoTokenError):
            self.common.verify_token(None)

    @patch('src.commands.common.Common.verify_token')
    def test_verify_token_expired(self, mock_verify_token):
        mock_verify_token.side_effect = InvalidTokenError
        with self.assertRaises(InvalidTokenError):
            self.common.verify_token('expired_token')

if __name__ == '__main__':
    unittest.main()