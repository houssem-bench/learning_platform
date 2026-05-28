from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class QuestionOut(BaseModel):
    id: int
    stem: str
    options: List[str]


class AttemptStartOut(BaseModel):
    attempt_id: int
    quiz_id: int
    started_at: datetime
    time_limit_seconds: int
    questions: List[QuestionOut]


class AttemptResumeOut(AttemptStartOut):
    remaining_seconds: int


class AttemptSubmitIn(BaseModel):
    answers: Dict[str, int]


class ExplanationOut(BaseModel):
    question_id: int
    selected_index: Optional[int]
    correct_index: int
    correct_text: str
    explanation: str
    is_correct: bool


class AttemptResultOut(BaseModel):
    attempt_id: int
    score: int
    total: int
    correct_count: int
    timed_out: bool
    submitted_at: datetime
    explanations: List[ExplanationOut]
