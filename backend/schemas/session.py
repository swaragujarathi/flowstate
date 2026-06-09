from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

class StudySessionResponse(BaseModel):

    id: int

    task_id: int

    user_id: int

    session_date: datetime

    planned_hours: float

    completed_hours: float

    is_completed: bool

    class Config:
        from_attributes = True

class SessionCompleteRequest(BaseModel):
    completed_hours: float = Field(
        ge=0
    )

class TodaySessionItem(BaseModel):

    session_id: int

    task_title: str

    planned_hours: float

    completed_hours: float

    is_completed: bool

class MissedSessionItem(BaseModel):

    session_id: int

    task_title: str

    planned_hours: float

    session_date: datetime