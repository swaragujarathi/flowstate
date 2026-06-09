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

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String)

    priority = Column(
        String,
        nullable=False,
        default="Medium"
    )

    estimated_hours = Column(
        Integer,
        nullable=False
    )

    completed_hours = Column(
        Integer,
        nullable=False,
        default=0
    )

    is_completed = Column(
        Boolean,
        nullable=False,
        default=False
    )

    deadline = Column(DateTime)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="tasks"
    )

    study_sessions = relationship(
    "StudySession",
    back_populates="task"
    )