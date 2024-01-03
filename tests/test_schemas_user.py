import unittest
from pydantic import ValidationError
from src.schemas.user import UserCreate

class TestUserSchemas(unittest.TestCase):

    def test_valid_user_create(self):
        user_data = {
            "email": "test@example.com",
            "password": "strongpassword",
            "name": "Test User"
        }
        user = UserCreate(**user_data)
        self.assertEqual(user.email, user_data["email"])
        self.assertEqual(user.name, user_data["name"])

    def test_invalid_user_create(self):
        user_data = {
            "email": "notanemail",
            "password": "weak"
        }
        with self.assertRaises(ValidationError):
            UserCreate(**user_data)

if __name__ == '__main__':
    unittest.main()
