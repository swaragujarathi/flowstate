from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]= None
    priority: Literal["Low", "Medium", "High"] = "Medium"
    estimated_hours: int
    deadline: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    estimated_hours: int
    completed_hours: int
    is_completed: bool
    deadline: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    completed_hours: int = Field(ge=0)

class TaskStatsResponse(BaseModel):
    task_id: int
    title: str

    estimated_hours: int
    completed_hours: int

    remaining_hours: int

    completion_percentage: float

    is_completed: bool

class SchedulePreviewItem(BaseModel):

    task_id: int

    title: str

    priority: str

    remaining_hours: int

    days_left: int

    required_hours_per_day: float

    urgency_score: float

    deadline: datetime

class DailyScheduleItem(BaseModel):
    task_id: int

    title: str

    priority: str

    hours_today: float

class WeeklyScheduleItem(BaseModel):
    date: str

    task_id: int

    title: str

    hours: float