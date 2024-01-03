import unittest
from datetime import timedelta
from your_project.utils.token import create_access_token, decode_access_token

class TestUtilsToken(unittest.TestCase):

    def test_create_access_token(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        self.assertIsNotNone(token)

    def test_decode_access_token(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        decoded_data = decode_access_token(token)
        self.assertEqual(decoded_data["sub"], "test@example.com")

    def test_expired_access_token(self):
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        decoded_data = decode_access_token(token)
        self.assertIsNone(decoded_data)

if __name__ == '__main__':
    unittest.main()
