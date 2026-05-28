from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(128), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500), default="", nullable=False)
    time_limit_seconds = Column(Integer, default=1800, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    attempts = relationship("Attempt", back_populates="quiz")
