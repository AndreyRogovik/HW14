from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags
from src.services.auth import auth_service

router = APIRouter(prefix='/tags', tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_tags function returns a list of tags.

    :param skip: int: Skip the first n tags
    :param limit: int: Limit the number of tags returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the auth_service
    :return: A list of tags
    :doc-author: Trelent
    """
    tags = await repository_tags.get_tags(skip, limit, current_user, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(tag_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_tag function will return a single tag from the database.
        The function takes in an integer, which is the id of the tag to be returned.
        It also takes in a Session object and a User object, both of which are used by
        other functions that read_tag calls.

    :param tag_id: int: Specify the id of the tag to be read
    :param db: Session: Pass the database session to the function
    :param current_user: User: Ensure that the user is authenticated
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(body: TagModel, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):

    """
    The create_tag function creates a new tag in the database.

    :param body: TagModel: Pass the request body to the function
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user who created the tag
    :return: A tag object
    :doc-author: Trelent
    """
    return await repository_tags.create_tag(body, current_user, db)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(body: TagModel, tag_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):

    """
    The update_tag function updates a tag in the database.
        The function takes three arguments:
            - body: A TagModel object containing the new values for the tag.
            - tag_id: An integer representing the ID of an existing tag to be updated.  This is passed as part of a URL path parameter, e.g., /tags/{tag_id}.
            - db (optional): A Session object that represents an open connection to a PostgreSQL database instance, which will be used by SQLAlchemy's ORM layer to perform CRUD operations on tags and their relationships with other entities in our application's

    :param body: TagModel: Pass in the new tag information
    :param tag_id: int: Specify the id of the tag to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: An updated tag
    :doc-author: Trelent
    """
    tag = await repository_tags.update_tag(tag_id, body, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(tag_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):

    """
    The remove_tag function removes a tag from the database.
        The function takes in an integer representing the id of the tag to be removed,
        and returns a dictionary containing information about that tag.

    :param tag_id: int: Get the tag id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is logged in
    :return: The tag that was removed
    :doc-author: Trelent
    """
    tag = await repository_tags.remove_tag(tag_id, current_user, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag
