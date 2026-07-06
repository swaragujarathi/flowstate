from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    text: str = Field(
        min_length=1,
        description="Natural language study plan."
    )


class ParsedTask(BaseModel):
    title: str
    estimated_hours: float = Field(gt=0)
    priority: Literal["High", "Medium", "Low"]
    difficulty: Literal["Easy", "Medium", "Hard"]
    deadline: date | None = None


class AIParseResponse(BaseModel):
    tasks: list[ParsedTask]