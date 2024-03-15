import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Note, Tag, User
from src.schemas import TagModel, TagResponse
from src.repository.tags import (
    get_tags,
    get_tag,
    create_tag,
    update_tag,
    remove_tag,

)


class TestTags(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_notes(self):
        tags = [Tag(), Tag(), Tag()]
        self.session.query().filter().offset().limit().all.return_value = tags
        result = await get_tags(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, tags)

    async def test_get_tag_found(self):
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = await get_tag(tag_id=1, user=self.user, db=self.session)
        self.assertEqual(result, tag)

    async def test_get_tag_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_tag(tag_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_tag(self):
        body = TagModel(name="test_tag")
        result = await create_tag(body=body, user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_tag_found(self):
        tag = Tag()
        self.session.query().filter().first.return_value = tag
        result = await remove_tag(tag_id=1, user=self.user, db=self.session)
        self.assertEqual(result, tag)

    async def test_remove_tag_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_tag(tag_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    # async def test_update_tag_found(self):
    #     body = TagModel(name="test_tag")
    #     tag = Tag(body=body)
    #     self.session.query().filter().first.return_value = tag
    #     self.session.commit.return_value = None
    #     result = await update_tag(tag_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, tag)

    async def test_update_tag_not_found(self):
        body = TagModel(name="new_test_tag")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_tag(tag_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

