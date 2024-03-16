from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate, NoteResponse
from src.repository import notes as repository_notes
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix='/notes', tags=["notes"])


@router.get("/", response_model=List[NoteResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_notes function returns a list of notes.

    :param skip: int: Skip the first n notes
    :param limit: int: Limit the number of notes returned
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A list of notes
    :doc-author: Trelent
    """
    notes = await repository_notes.get_notes(skip, limit, current_user, db)
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):

    """
    The read_note function is used to read a note by its ID.

    :param note_id: int: Specify the type of the parameter and to give it a name
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A note object
    :doc-author: Trelent
    """
    note = await repository_notes.get_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(body: NoteModel, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):

    """
    The create_note function creates a new note in the database.

    :param body: NoteModel: Get the body of the request
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user who is currently logged in
    :return: A note object
    :doc-author: Trelent
    """
    return await repository_notes.create_note(body, current_user, db)


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(body: NoteUpdate, note_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):

    """
    The update_note function updates a note in the database.
        The function takes three arguments:
            - body: A NoteUpdate object containing the new values for the note.
            - note_id: An integer representing the ID of an existing note to be updated.
                This is passed as a path parameter, not as part of JSON request body.
                It's also validated by FastAPI using Pydantic models and OpenAPI schemas, so it will always be an integer when it reaches this function (unless there's some other bug).

    :param body: NoteUpdate: Get the data that is being passed in from the request body
    :param note_id: int: Identify the note to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is currently logged in
    :return: A note object
    :doc-author: AR
    """
    note = await repository_notes.update_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=NoteResponse)
async def update_status_note(body: NoteStatusUpdate, note_id: int, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):

    """
    The update_status_note function updates the status of a note.
        The function takes in a NoteStatusUpdate object, which contains the new status for the note.
        It also takes in an integer representing the id of the note to be updated and two optional parameters:
            - db: A database session that is used to query data from our database (defaults to Depends(get_db))
            - current_user: The user who is making this request (defaults to Depends(auth_service.get_current_user))

    :param body: NoteStatusUpdate: Get the status of the note from the request body
    :param note_id: int: Get the note id from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user who is logged in
    :return: A note object
    :doc-author: Trelent
    """
    note = await repository_notes.update_status_note(note_id, body, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.delete("/{note_id}", response_model=NoteResponse)
async def remove_note(note_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):

    """
    The remove_note function removes a note from the database.

    :param note_id: int: Specify the note to be removed
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user that is currently logged in
    :return: A note object
    :doc-author: Trelent
    """
    note = await repository_notes.remove_note(note_id, current_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note
