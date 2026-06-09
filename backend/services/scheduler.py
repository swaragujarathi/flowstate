from sqlalchemy.orm import Session
from datetime import datetime
from models import StudySession

def get_priority_weight(priority: str):

    weights = {
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    return weights.get(priority, 2)

def session_exists_today(
    db: Session,
    task_id: int,
    user_id: int
):
    today = datetime.utcnow().date()

    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.task_id == task_id,
            StudySession.user_id == user_id
        )
        .all()
    )

    return any(
        session.session_date.date() == today
        for session in sessions
    )