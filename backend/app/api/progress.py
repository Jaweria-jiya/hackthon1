from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select # Import select
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession

from app.db.session import get_db
from app.db.models import progress as db_models
from app.db.models import user as user_db_models # Import user model to validate user_id
from app.schemas import progress as schemas

router = APIRouter()

class ProgressCreateWithUser(schemas.ProgressCreate):
    user_id: uuid.UUID

@router.post("/progress/", response_model=schemas.Progress, status_code=status.HTTP_201_CREATED)
async def create_progress(progress: ProgressCreateWithUser, db: AsyncSession = Depends(get_db)):
    # Validate user_id
    stmt = select(user_db_models.User).where(user_db_models.User.id == progress.user_id)
    result = await db.execute(stmt)
    user_exists = result.scalar_one_or_none()
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_progress = db_models.Progress(
        user_id=progress.user_id,
        week_number=progress.week_number,
        completion_percent=progress.completion_percent
    )
    db.add(db_progress)
    await db.commit()
    await db.refresh(db_progress)
    return db_progress

@router.get("/progress/", response_model=List[schemas.Progress])
async def read_progress_entries(user_id: uuid.UUID = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.Progress)
    if user_id:
        stmt = stmt.where(db_models.Progress.user_id == user_id)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    progress_entries = result.scalars().all()
    return progress_entries

@router.get("/progress/{progress_id}", response_model=schemas.Progress)
async def read_progress_entry(progress_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.Progress).where(db_models.Progress.id == progress_id)
    result = await db.execute(stmt)
    db_progress = result.scalar_one_or_none()
    if db_progress is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress entry not found")
    return db_progress

@router.put("/progress/{progress_id}", response_model=schemas.Progress)
async def update_progress(progress_id: uuid.UUID, progress: ProgressCreateWithUser, db: AsyncSession = Depends(get_db)):
    stmt_progress = select(db_models.Progress).where(db_models.Progress.id == progress_id)
    result_progress = await db.execute(stmt_progress)
    db_progress = result_progress.scalar_one_or_none()
    if db_progress is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress entry not found")

    # Optional: Check if the user_id in the request matches the progress's user_id if security was in scope.
    if progress.user_id:
        stmt_user = select(user_db_models.User).where(user_db_models.User.id == progress.user_id)
        result_user = await db.execute(stmt_user)
        user_exists = result_user.scalar_one_or_none()
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found for reassignment")
        db_progress.user_id = progress.user_id
        
    db_progress.week_number = progress.week_number
    db_progress.completion_percent = progress.completion_percent
    await db.commit()
    await db.refresh(db_progress)
    return db_progress

@router.delete("/progress/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress(progress_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.Progress).where(db_models.Progress.id == progress_id)
    result = await db.execute(stmt)
    db_progress = result.scalar_one_or_none()
    if db_progress is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Progress entry not found")
    
    await db.delete(db_progress)
    await db.commit()
    return {"ok": True}
