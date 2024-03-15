from typing import Union

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:

    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Pass in the email address of the user we want to retrieve
    :param db: Session: Pass in the database session
    :return: The first user in the database with the given email address
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:

    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Pass in the usermodel object that is created from the request body
    :param db: Session: Access the database
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: Union[str, None], db: Session) -> None:

    """
    The update_token function updates the refresh token for a user in the database.

    :param user: User: Identify the user to update
    :param token: Union[str: Define the type of data that is expected to be passed into the function
    :param None]: Indicate that the token parameter can be either a string or none
    :param db: Session: Pass the database session to the function
    :return: Nothing
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:

    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Pass the email address of the user to be confirmed
    :param db: Session: Pass the database session into the function
    :return: Nothing, but it sets the user's confirmed status to true
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:

    """
    The update_avatar function updates the avatar of a user in the database.

    :param email: Identify the user to update
    :param url: str: Pass the url of the avatar image to be updated
    :param db: Session: Pass the database session to the function
    :return: The updated user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
