from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select # Import select
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession

from app.db.session import get_db
from app.db.models import note as db_models
from app.db.models import user as user_db_models # Import user model to validate user_id
from app.schemas import note as schemas

router = APIRouter()

class NoteCreateWithUser(schemas.NoteCreate):
    user_id: uuid.UUID

@router.post("/notes/", response_model=schemas.Note, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreateWithUser, db: Session = Depends(get_db)):
    # Validate user_id
    stmt = select(user_db_models.User).where(user_db_models.User.id == note.user_id)
    result = await db.execute(stmt)
    user_exists = result.scalar_one_or_none()
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_note = db_models.Note(user_id=note.user_id, content=note.content)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note

@router.get("/notes/", response_model=List[schemas.Note])
async def read_notes(user_id: uuid.UUID = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.Note)
    if user_id:
        stmt = stmt.where(db_models.Note.user_id == user_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    notes = result.scalars().all()
    return notes

@router.get("/notes/{note_id}", response_model=schemas.Note)
async def read_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.Note).where(db_models.Note.id == note_id)
    result = await db.execute(stmt)
    db_note = result.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note

@router.put("/notes/{note_id}", response_model=schemas.Note)
async def update_note(note_id: uuid.UUID, note: NoteCreateWithUser, db: AsyncSession = Depends(get_db)):
    stmt_note = select(db_models.Note).where(db_models.Note.id == note_id)
    result_note = await db.execute(stmt_note)
    db_note = result_note.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    # Optional: Check if the user_id in the request matches the note's user_id if security was in scope.
    # For now, we allow changing content. If user_id is changed, it reassigns the note.
    if note.user_id:
        stmt_user = select(user_db_models.User).where(user_db_models.User.id == note.user_id)
        result_user = await db.execute(stmt_user)
        user_exists = result_user.scalar_one_or_none()
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found for reassignment")
        db_note.user_id = note.user_id
    
    db_note.content = note.content
    await db.commit()
    await db.refresh(db_note)
    return db_note

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.Note).where(db_models.Note.id == note_id)
    result = await db.execute(stmt)
    db_note = result.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    
    await db.delete(db_note)
    await db.commit()
    return {"ok": True}
