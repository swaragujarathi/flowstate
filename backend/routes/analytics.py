from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import engine, Base, get_db
from models import User, Task, StudySession
from schemas import AnalyticsOverview, ProductivityResponse, StreakResponse, WeeklyAnalyticsItem
from auth import get_current_user

router = APIRouter(
    tags=["Analytics"]
)

@router.get(
    "/analytics/overview",
    response_model=AnalyticsOverview
)
def analytics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id
        )
        .all()
    )

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id == current_user.id
        )
        .all()
    )

    total_tasks = len(tasks)

    completed_tasks = sum(
        1
        for task in tasks
        if task.is_completed
    )

    if total_tasks == 0:
        completion_rate = 0
    else:
        completion_rate = (
            completed_tasks /
            total_tasks
        ) * 100

    total_hours_studied = sum(
        session.completed_hours
        for session in sessions
    )

    today = datetime.utcnow().date()

    missed_sessions = sum(
        1
        for session in sessions
        if (
            session.session_date.date() < today
            and
            not session.is_completed
        )
    )

    return {
        "total_tasks": total_tasks,

        "completed_tasks": completed_tasks,

        "completion_rate": round(completion_rate,2),

        "total_hours_studied": round(total_hours_studied, 2),

        "missed_sessions": missed_sessions
    }

@router.get(
    "/analytics/productivity",
    response_model=ProductivityResponse
)
def get_productivity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id ==
            current_user.id
        )
        .all()
    )

    planned_hours = sum(
        session.planned_hours
        for session in sessions
    )

    completed_hours = sum(
        session.completed_hours
        for session in sessions
    )

    if planned_hours == 0:
        productivity_score = 0
    else:
        productivity_score = (
            completed_hours /
            planned_hours
        ) * 100

    return {
        "planned_hours": round(
            planned_hours,
            2
        ),

        "completed_hours": round(
            completed_hours,
            2
        ),

        "productivity_score": round(
            productivity_score,
            2
        )
    }

from datetime import datetime, timedelta

@router.get(
    "/analytics/streak",
    response_model=StreakResponse
)
def get_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id == current_user.id,
            StudySession.completed_hours > 0
        )
        .all()
    )

    study_dates = {
        session.session_date.date()
        for session in sessions
    }

    today = datetime.utcnow().date()

    streak = 0

    current_day = today

    while current_day in study_dates:

        streak += 1

        current_day = (
            current_day -
            timedelta(days=1)
        )

    return {
        "current_streak": streak
    }

@router.get(
    "/analytics/weekly",
    response_model=list[WeeklyAnalyticsItem]
)
def get_weekly_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    today = datetime.utcnow().date()

    weekly_data = {}

    for i in range(6, -1, -1):

        day = (
            today -
            timedelta(days=i)
        )

        weekly_data[day] = 0

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id ==
            current_user.id
        )
        .all()
    )

    for session in sessions:

        session_day = (
            session.session_date.date()
        )

        if session_day in weekly_data:

            weekly_data[
                session_day
            ] += session.completed_hours

    result = []

    for day, hours in weekly_data.items():

        result.append(
            {
                "date": str(day),
                "hours": round(hours, 2)
            }
        )

    return result