from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:

    """
    The get_contacts function returns a list of contacts for the user.

    :param skip: int: Skip a number of rows in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Filter the contacts by user
    :param db: Session: Pass the database session to the function
    :return: A list of contacts for the given user
    :doc-author: AR
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact function takes in a contact_id and user, and returns the contact with that id.
        Args:
            contact_id (int): The id of the desired Contact object.
            user (User): The User object associated with this request.

    :param contact_id: int: Specify the contact id that is being searched for
    :param user: User: Get the user id of the current logged in user
    :param db: Session: Pass the database session to the function
    :return: A contact object for a given user, if it exists
    :doc-author: AR
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactCreate, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactCreate): The contact to create.
            user (User): The current user, who is creating the contact.

    :param body: ContactCreate: Get the data from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: The contact object
    :doc-author: AR
    """
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email,
                      phone_number=body.phone_number, birthday=body.birthday, additional_data=body.additional_data, user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int,  user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
    Args:
    contact_id (int): The id of the contact to be removed.
    user (User): The user who is removing the contact.  This is used to ensure that only contacts belonging to this
    user are removed, and not contacts belonging to other users with similar names or email addresses.

    :param contact_id: int: Identify the contact to be deleted
    :param user: User: Identify the user who is making the request
    :param db: Session: Pass in the database session
    :return: The contact object that was removed from the database
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if Contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactUpdate): The updated information for the specified contact.
            user (User): The user who is making this request, used to verify that they are authorized to make this change.

    :param contact_id: int: Specify the contact to be deleted
    :param body: ContactUpdate: Pass in the updated contact information
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


