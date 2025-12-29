from typing import List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select # Import select
from sqlalchemy.ext.asyncio import AsyncSession # Import AsyncSession

from app.db.session import get_db
from app.db.models import user as db_models
from app.schemas import user as schemas

router = APIRouter()

@router.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.User).where(db_models.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: uuid.UUID, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.User).where(db_models.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.email:
        db_user.email = user.email
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(db_models.User).where(db_models.User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    await db.delete(db_user)
    await db.commit()
    return {"ok": True}
