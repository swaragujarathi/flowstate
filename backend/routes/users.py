from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import User
from schemas import StudyHoursUpdate
from auth import get_current_user

router = APIRouter(
    tags=["Users"]
)

@router.patch("/users/study-hours")
def update_study_hours(
    data: StudyHoursUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    current_user.daily_study_hours = (
        data.daily_study_hours
    )

    db.commit()
    db.refresh(current_user)

    return {
        "daily_study_hours":
        current_user.daily_study_hours
    }