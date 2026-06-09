from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import User, Task, StudySession
from schemas import StudySessionResponse, SessionCompleteRequest, TodaySessionItem, MissedSessionItem
from auth import get_current_user

router = APIRouter(
    tags=["Sessions"]
)

@router.post("/sessions/{task_id}", response_model=StudySessionResponse)
def create_session(
    task_id: int, 
    planned_hours: float, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=404, 
            detail="Task not found"
        )
    
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to modify this task"
        )
    
    session = StudySession(
        task_id=task.id,
        user_id=current_user.id,
        session_date=datetime.utcnow(),
        planned_hours=planned_hours
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.get(
    "/sessions/today",
    response_model=list[TodaySessionItem]
)
def get_today_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id ==
            current_user.id
        )
        .all()
    )

    result = []

    for session in sessions:

        if session.session_date.date() != today:
            continue

        result.append(
            {
                "session_id": session.id,
                "task_title": session.task.title,
                "planned_hours": session.planned_hours,
                "completed_hours":
                session.completed_hours,
                "is_completed":
                session.is_completed
            }
        )

    return result

@router.patch(
    "/sessions/{session_id}/complete",
    response_model=StudySessionResponse
)
def complete_session(
    session_id: int,
    data: SessionCompleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = (
        db.query(StudySession)
        .filter(
            StudySession.id == session_id,
            StudySession.user_id ==
            current_user.id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    session.completed_hours = (
        data.completed_hours
    )

    if (
        session.completed_hours >=
        session.planned_hours
    ):
        session.is_completed = True

    task = session.task

    task.completed_hours += (
        data.completed_hours
    )

    if (
        task.completed_hours >=
        task.estimated_hours
    ):
        task.is_completed = True

    db.commit()

    db.refresh(session)

    return session

@router.get(
    "/sessions/missed",
    response_model=list[MissedSessionItem]
)
def get_missed_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id ==
            current_user.id
        )
        .all()
    )

    missed = []

    for session in sessions:

        if (
            session.session_date.date() < today
            and
            not session.is_completed
        ):

            missed.append(
                {
                    "session_id": session.id,
                    "task_title":
                    session.task.title,

                    "planned_hours":
                    session.planned_hours,

                    "session_date":
                    session.session_date
                }
            )

    return missed