from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Float
)
from sqlalchemy.orm import relationship
from database import Base

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    session_date = Column(
        DateTime,
        nullable=False
    )

    planned_hours = Column(
        Float,
        nullable=False
    )

    completed_hours = Column(
        Float,
        default=0
    )

    is_completed = Column(
        Boolean,
        default=False
    )

    user = relationship(
        "User",
        back_populates="study_sessions"
    )

    task = relationship(
        "Task",
        back_populates="study_sessions"
    )