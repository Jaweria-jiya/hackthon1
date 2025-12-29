from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import activity as activity_schema
from app.db import models
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/track", response_model=activity_schema.UserActivityLog)
def track_user_activity(
    *,
    db: Session = Depends(get_db),
    activity_in: activity_schema.UserActivityLogCreate,
    current_user: models.User = Depends(get_current_user)
):
    """
    Track user activity.
    """
    if activity_in.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Cannot track activity for another user.",
        )
    
    activity_log = models.UserActivityLog(
        user_id=activity_in.user_id,
        email=activity_in.email,
        action=activity_in.action,
        resource_id=activity_in.resource_id
    )
    db.add(activity_log)
    db.commit()
    db.refresh(activity_log)
    return activity_log
