from typing import List, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Tag, User
from src.schemas import TagModel


async def get_tags(skip: int, limit: int, user: User, db: Session) -> List[Tag]:
    """
    The get_tags function returns a list of tags for the user.

    :param skip: int: Skip a number of tags in the database
    :param limit: int: Limit the number of tags that are returned
    :param user: User: Get the user's id
    :param db: Session: Pass the database session to the function
    :return: A list of tags
    :doc-author: AR
    """
    return db.query(Tag).filter(Tag.user_id == user.id).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, user: User, db: Session) -> Tag:
    """
    The get_tag function takes in a tag_id and user object, and returns the Tag object with that id.
        If no such tag exists, it raises an HTTPException.

    :param tag_id: int: Get the tag with that id
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A tag object based on the id and user
    :doc-author: Trelent
    """
    return db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()


async def create_tag(body: TagModel, user: User, db: Session) -> Tag:
    """
    The create_tag function creates a new tag in the database.

    :param body: TagModel: Get the name of the tag from the request body
    :param user: User: Get the user_id from the logged in user
    :param db: Session: Pass the database session to the function
    :return: A tag object
    :doc-author: Trelent
    """
    tag = Tag(name=body.name, user_id=user.id)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, user: User, db: Session) -> Union[Tag, None]:
    """
    The update_tag function updates a tag in the database.
        Args:
            tag_id (int): The id of the tag to update.
            body (TagModel): The new data for the updated Tag object.  This is a Pydantic model, which means it has been validated against its schema before being passed into this function.  See schemas/tag_model for more information on what fields are required and how they are validated by Pydantic models.
            user (User): A User object representing who is making this request to update a Tag object in our database; we need this so that we can

    :param tag_id: int: Identify the tag to be deleted
    :param body: TagModel: Get the new tag name from the request body
    :param user: User: Ensure that the user is authorized to update the tag
    :param db: Session: Access the database
    :return: The updated tag if it exists, otherwise none
    :doc-author: Trelent
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        tag .name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, user: User, db: Session) -> Union[Tag, None]:

    """
    The remove_tag function removes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be removed.
            user (User): The user who owns the tags being removed.  This is used for security purposes, so that users can only remove their own tags and not those of other users.
            db (Session): A connection to our database, which we use to query and delete data from it.

    :param tag_id: int: Specify the tag to be deleted
    :param user: User: Get the user's id
    :param db: Session: Access the database
    :return: The tag that was removed
    :doc-author: Trelent
    """
    tag = db.query(Tag).filter(and_(Tag.id == tag_id, Tag.user_id == user.id)).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
