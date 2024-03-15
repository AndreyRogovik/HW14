import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactCreate, ContactUpdate, ContactResponse
from src.repository.contacts import get_contacts, get_contact, create_contact, remove_contact, update_contact


class TestContactController(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactCreate(first_name="Ivan", last_name="Petriv", email="test@email.com", phone_number="+380123456789")
        result = await self.controller.create(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_found(self):
        body = ContactUpdate(first_name="Avr", phone="+380999999999")
        contact = Contact(first_name="Natalka", last_name="Poltavka")
        self.session.query().filter().first.return_value = contact
        result = await update_contact(id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_not_found(self):
        body = ContactUpdate(first_name="Ivan", phone="+380331231234")
        self.session.query().filter().first.return_value = None
        result = await update_contact(id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
