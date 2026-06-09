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

class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # User's full name or username
    name = Column(String, nullable=False)
    
    # Unique email so two people can't register with the same email
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Store hashed version of password
    hashed_password = Column(String, nullable=False)
    
    # Useful for features like email verification
    is_active = Column(Boolean, default=True)

    tasks= relationship(
        "Task",
        back_populates="owner"
    )

    daily_study_hours = Column(
    Integer,
    nullable=False,
    default=5
    )

    study_sessions = relationship(
    "StudySession",
    back_populates="user"
    )