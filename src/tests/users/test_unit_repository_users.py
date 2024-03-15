import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.repository.users import get_user_by_email, create_user, confirmed_email, update_avatar
from src.database.models import User
from src.schemas import UserModel, UserDb, UserResponse


class TestAuthControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)

    async def test_get_user_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test@mail.com", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="test@mail.com", db=self.session)
        self.assertIsNone(result)

    async def test_confirm_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await confirmed_email(email="test@mail.com", db=self.session)
        self.assertIsNone(result)

    async def test_create(self):
        body = UserModel(username="username", email="test@mail.com", password="123123123")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(body.username, result.username)
        self.assertEqual(body.email, result.email)
        self.assertEqual(body.password, result.password)


class TestUserController(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)

    async def test_update_avatar(self):
        email = "test@mail.com"
        url = "https://test.url"
        result = await update_avatar(email=email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)


if __name__ == "__main__":
    unittest.main()
