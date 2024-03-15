from typing import List, Union

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Note, Tag, User
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(skip: int, limit: int, user: User, db: Session) -> List[Note]:
    """
    The get_notes function returns a list of notes for the given user.
    :param skip: int: Skip the first n notes
    :param limit: int: Limit the number of notes that are returned
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: A list of notes for a particular user
    :doc-author: AR
    """
    return db.query(Note).filter(Note.user_id == user.id).offset(skip).limit(limit).all()


async def get_note(note_id: int, user: User, db: Session) -> Note:
    """
    The get_note function takes in a note_id and user, and returns the Note object with that id.
        Args:
            note_id (int): The id of the Note to be retrieved.
            user (User): The User who owns the Note to be retrieved.

    :param note_id: int: Get the note with the given id
    :param user: User: Get the user who is making the request
    :param db: Session: Pass the database session to the function
    :return: A note object from the database
    :doc-author: AR
    """
    return db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()


async def create_note(body: NoteModel, user: User, db: Session) -> Note:
    """
    The create_note function creates a new note in the database.
    :param body: NoteModel: Get the title, description and tags from the request body
    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: A note object
    :doc-author: AR
    """
    tags = db.query(Tag).filter(and_(Tag.id.in_(body.tags), Tag.user_id == user.id)).all()
    note = Note(title=body.title, description=body.description, tags=tags, user=user)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def remove_note(note_id: int, user: User, db: Session) -> Union[Note, None]:
    """
    The remove_note function removes a note from the database.
        Args:
            note_id (int): The id of the note to be removed.
            user (User): The user who owns the note to be removed.
            db (Session): A connection to our database, used for querying and deleting notes.

    :param note_id: int: Identify the note to be removed
    :param user: User: Identify the user who is making the request
    :param db: Session: Access the database
    :return: The note that was removed
    :doc-author: AR
    """
    note = db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        db.delete(note)
        db.commit()
    return note


async def update_note(note_id: int, body: NoteUpdate, user: User, db: Session) -> Union[Note, None]:

    """
    The update_note function updates a note in the database.

    :param note_id: int: Identify the note to be deleted
    :param body: NoteUpdate: Pass in the updated note information
    :param user: User: Check if the user is authorized to make changes to the note
    :param db: Session: Access the database
    :return: The updated note if the user is authorized to update it, otherwise none
    :doc-author: AR
    """
    note = db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        tags = db.query(Tag).filter(and_(Tag.id.in_(body.tags), Note.user_id == user.id)).all()
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        db.commit()
    return note


async def update_status_note(note_id: int, body: NoteStatusUpdate, user: User, db: Session) -> Union[Note, None]:

    """
    The update_status_note function updates a note in the database.

    :param note_id: int: Identify the note to be deleted
    :param body: NoteStatusUpdate: Pass in the updated note information
    :param user: User: Check if the user is authorized to make changes to the note
    :param db: Session: Access the database
    :return: The updated note if the user is authorized to update it, otherwise none
    :doc-author: AR
    """
    note = db.query(Note).filter(and_(Note.id == note_id, Note.user_id == user.id)).first()
    if note:
        note.done = body.done
        db.commit()
    return note
