from pydantic import BaseModel


class QuizOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    time_limit_seconds: int
    question_count: int
