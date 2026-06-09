from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class StudyHoursUpdate(BaseModel):
    daily_study_hours: int = Field(
        ge=1,
        le=24
    )