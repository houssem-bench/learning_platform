from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False, index=True)
    seed = Column(Integer, nullable=False)
    started_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    score = Column(Integer, nullable=True)
    total = Column(Integer, nullable=True)
    time_limit_seconds = Column(Integer, nullable=False)
    timed_out = Column(Boolean, default=False, nullable=False)
    question_order = Column(JSON, nullable=False)
    option_orders = Column(JSON, nullable=False)
    answers = Column(JSON, nullable=True)

    user = relationship("User", back_populates="attempts")
    quiz = relationship("Quiz", back_populates="attempts")
