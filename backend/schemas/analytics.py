from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

class AnalyticsOverview(BaseModel):

    total_tasks: int

    completed_tasks: int

    completion_rate: float

    total_hours_studied: float

    missed_sessions: int

class ProductivityResponse(BaseModel):

    planned_hours: float

    completed_hours: float

    productivity_score: float

class StreakResponse(BaseModel):

    current_streak: int

class WeeklyAnalyticsItem(BaseModel):

    date: str

    hours: float