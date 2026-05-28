from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.attempt import Attempt
from app.models.question import Question
from app.models.user import User
from app.schemas.attempt import (
    AttemptResultOut,
    AttemptResumeOut,
    AttemptSubmitIn,
    ExplanationOut,
    QuestionOut,
)

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.get("/{attempt_id}", response_model=AttemptResumeOut)
def get_attempt(
    attempt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AttemptResumeOut:
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id, Attempt.user_id == current_user.id)
        .first()
    )
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found"
        )
    if attempt.submitted_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt already submitted",
        )

    now = datetime.now(timezone.utc)
    elapsed = (now - attempt.started_at).total_seconds()
    remaining = max(int(attempt.time_limit_seconds - elapsed), 0)

    questions = (
        db.query(Question)
        .filter(Question.id.in_(attempt.question_order))
        .all()
    )
    questions_by_id = {q.id: q for q in questions}
    question_payload: list[QuestionOut] = []
    for question_id in attempt.question_order:
        question = questions_by_id.get(question_id)
        if not question:
            continue
        order = attempt.option_orders.get(
            str(question_id), list(range(len(question.options)))
        )
        options = [question.options[i] for i in order]
        question_payload.append(
            QuestionOut(id=question.id, stem=question.stem, options=options)
        )

    return AttemptResumeOut(
        attempt_id=attempt.id,
        quiz_id=attempt.quiz_id,
        started_at=attempt.started_at,
        time_limit_seconds=attempt.time_limit_seconds,
        remaining_seconds=remaining,
        questions=question_payload,
    )


@router.post("/{attempt_id}/submit", response_model=AttemptResultOut)
def submit_attempt(
    attempt_id: int,
    payload: AttemptSubmitIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AttemptResultOut:
    attempt = (
        db.query(Attempt)
        .filter(Attempt.id == attempt_id, Attempt.user_id == current_user.id)
        .first()
    )
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found"
        )
    if attempt.submitted_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt already submitted",
        )

    now = datetime.now(timezone.utc)
    elapsed = (now - attempt.started_at).total_seconds()
    timed_out = elapsed > attempt.time_limit_seconds

    answers = payload.answers or {}
    score = 0
    total = len(attempt.question_order)
    explanations: list[ExplanationOut] = []

    for question_id in attempt.question_order:
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            continue
        option_order = attempt.option_orders.get(
            str(question_id), list(range(len(question.options)))
        )
        selected_display_index = answers.get(str(question_id))
        is_correct = False
        if selected_display_index is not None and 0 <= selected_display_index < len(
            option_order
        ):
            selected_original_index = option_order[selected_display_index]
            if selected_original_index == question.correct_index:
                is_correct = True

        if is_correct:
            score += 1

        correct_display_index = option_order.index(question.correct_index)
        explanations.append(
            ExplanationOut(
                question_id=question_id,
                selected_index=selected_display_index,
                correct_index=correct_display_index,
                correct_text=question.options[question.correct_index],
                explanation=question.explanation,
                is_correct=is_correct,
            )
        )

    attempt.submitted_at = now
    attempt.score = score
    attempt.total = total
    attempt.timed_out = timed_out
    attempt.answers = answers
    db.commit()

    return AttemptResultOut(
        attempt_id=attempt.id,
        score=score,
        total=total,
        correct_count=score,
        timed_out=timed_out,
        submitted_at=attempt.submitted_at,
        explanations=explanations,
    )
