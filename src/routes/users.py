from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from src import settings
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_users_me function returns the current user's information.

    :param current_user: User: Get the current user
    :return: The current user
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):

    """
    The update_avatar_user function is used to update the avatar of a user.
        The function takes in an UploadFile object, which is a file that has been uploaded by the client.
        It also takes in the current_user and db objects as dependencies.

    :param file: UploadFile: Get the file from the request
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the function
    :return: The updated user
    :doc-author: Trelent
    """
    cloudinary.config(
        cloud_name=settings.CLOUD_NAME,
        api_key=settings.API_KEY,
        api_secret=settings.API_SECRET,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
