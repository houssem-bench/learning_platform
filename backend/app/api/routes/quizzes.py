import random
import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.attempt import Attempt
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.user import User
from app.schemas.attempt import AttemptStartOut, QuestionOut
from app.schemas.quiz import QuizOut

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("", response_model=list[QuizOut])
def list_quizzes(db: Session = Depends(get_db)) -> list[QuizOut]:
    quizzes = db.query(Quiz).all()
    results: list[QuizOut] = []
    for quiz in quizzes:
        results.append(
            QuizOut(
                id=quiz.id,
                slug=quiz.slug,
                title=quiz.title,
                description=quiz.description,
                time_limit_seconds=quiz.time_limit_seconds,
                question_count=len(quiz.questions),
            )
        )
    return results


@router.post("/{quiz_id}/attempts", response_model=AttemptStartOut)
def start_attempt(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AttemptStartOut:
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    questions = list(quiz.questions)
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz has no questions",
        )

    seed = time.time_ns()
    rng = random.Random(seed)
    question_order = [question.id for question in questions]
    rng.shuffle(question_order)

    option_orders: dict[str, list[int]] = {}
    for question in questions:
        indices = list(range(len(question.options)))
        rng.shuffle(indices)
        option_orders[str(question.id)] = indices

    attempt = Attempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        seed=seed,
        time_limit_seconds=quiz.time_limit_seconds,
        question_order=question_order,
        option_orders=option_orders,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    questions_by_id: dict[int, Question] = {q.id: q for q in questions}
    question_payload: list[QuestionOut] = []
    for question_id in question_order:
        question = questions_by_id[question_id]
        order = option_orders[str(question_id)]
        options = [question.options[i] for i in order]
        question_payload.append(
            QuestionOut(id=question.id, stem=question.stem, options=options)
        )

    return AttemptStartOut(
        attempt_id=attempt.id,
        quiz_id=quiz.id,
        started_at=attempt.started_at,
        time_limit_seconds=attempt.time_limit_seconds,
        questions=question_payload,
    )
