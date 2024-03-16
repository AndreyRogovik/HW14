from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.db import get_db
from src.schemas import ContactCreate, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=1000, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip a number of records
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_note function will return a single note from the database.
        The contact_id parameter is used to find the specific note in question.
        If no such contact exists, an HTTP 404 error is returned.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the auth_service
    :return: The contact that was found in the database
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id,current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=1000, seconds=60))])
async def create_contacts(body: ContactCreate, db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):

    """
    The create_contacts function creates a new contact in the database.

    :param body: ContactCreate: Get the data from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id of the logged in user
    :return: A contact object that is created in the database
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db),
                         curent_user: User = Depends(auth_service.get_current_user)):

    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactUpdate object containing the new values for the contact's fields.
            - contact_id: An integer representing the ID of an existing contact to be updated.
                This is passed as a path parameter, so it must be included in any request URL that calls this function.
            - db (optional): A Session object used to access and modify data stored in a database using SQLAlchemy ORM methods.

    :param body: ContactUpdate: Get the data from the request body
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database session to the repository_contacts
    :param curent_user: User: Get the current user
    :return: The updated contact, which is then returned to the client
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, curent_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         curent_user: User = Depends(auth_service.get_current_user)):

    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Get the database session
    :param curent_user: User: Get the current user from the database
    :return: The removed contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, curent_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


