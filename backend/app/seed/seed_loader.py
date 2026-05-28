import re
from pathlib import Path

from app.models.attempt import Attempt
from app.models.question import Question
from app.models.quiz import Quiz

LETTER_ORDER = "ABCD"
QUESTION_RE = re.compile(r"^(\d+)\.\s+(.*)$")
OPTION_RE = re.compile(r"^([A-D])\.\s+(.*)$")
CORR_RE = re.compile(r"^([A-D])\s*-\s*(.*)$")

SEED_DIR = Path(__file__).parent

QUIZ_SOURCES = [
    {
        "slug": "unity-qcu-v1",
        "title": "Unity QCU - Version 1 (Easy)",
        "description": "Unity and XR fundamentals.",
        "time_limit_seconds": 2700,
        "questions_file": "unity_v1_questions.txt",
        "corrections_file": "unity_v1_corrections.txt",
    },
    {
        "slug": "unity-qcu-v2",
        "title": "Unity QCU - Version 2 (Medium)",
        "description": "Intermediate Unity, VR, and AR troubleshooting.",
        "time_limit_seconds": 2700,
        "questions_file": "unity_v2_questions.txt",
        "corrections_file": "unity_v2_corrections.txt",
    },
    {
        "slug": "unity-qcu-v3",
        "title": "Unity QCU - Version 3 (Hard)",
        "description": "Advanced Unity, VR, and AR architecture.",
        "time_limit_seconds": 2700,
        "questions_file": "unity_v3_questions.txt",
        "corrections_file": "unity_v3_corrections.txt",
    },
    {
        "slug": "unity-qcu-v4",
        "title": "Unity QCU - Version 4 (Extra Hard)",
        "description": "Expert Unity, XR, and lifecycle troubleshooting.",
        "time_limit_seconds": 2700,
        "questions_file": "unity_v4_questions.txt",
        "corrections_file": "unity_v4_corrections.txt",
    },
    {
        "slug": "unity-qcu-v5",
        "title": "Unity QCU - Version 5 (Extra Hard - Trap)",
        "description": "Advanced VR/AR pitfalls and architecture traps.",
        "time_limit_seconds": 2700,
        "questions_file": "unity_v5_questions.txt",
        "corrections_file": "unity_v5_corrections.txt",
    },
]


def parse_questions_block(text: str) -> list[dict]:
    questions = []
    current = None
    header_seen = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not header_seen and not QUESTION_RE.match(line):
            header_seen = True
            continue
        match_q = QUESTION_RE.match(line)
        if match_q:
            if current:
                questions.append(current)
            current = {
                "number": int(match_q.group(1)),
                "stem": match_q.group(2).strip(),
                "options": [],
            }
            continue
        match_opt = OPTION_RE.match(line)
        if match_opt and current:
            current["options"].append(match_opt.group(2).strip())
    if current:
        questions.append(current)
    for question in questions:
        if len(question["options"]) != 4:
            raise ValueError(
                f"Expected 4 options in question {question['number']}, got {len(question['options'])}"
            )
    return questions


def parse_corrections_block(text: str) -> list[dict]:
    corrections = []
    header_seen = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if not header_seen:
            header_seen = True
            continue
        match_corr = CORR_RE.match(line)
        if match_corr:
            corrections.append(
                {
                    "letter": match_corr.group(1),
                    "explanation": match_corr.group(2).strip(),
                }
            )
    return corrections


def load_seed(db, replace: bool = False) -> dict:
    if replace:
        if db.query(Attempt).count() > 0:
            raise ValueError("Cannot re-import while attempts exist.")
        db.query(Question).delete()
        db.query(Quiz).delete()
        db.commit()

    imported = 0
    for source in QUIZ_SOURCES:
        existing = db.query(Quiz).filter(Quiz.slug == source["slug"]).first()
        if existing:
            continue
        questions_text = (SEED_DIR / source["questions_file"]).read_text(
            encoding="utf-8"
        )
        corrections_text = (SEED_DIR / source["corrections_file"]).read_text(
            encoding="utf-8"
        )
        questions = parse_questions_block(questions_text)
        corrections = parse_corrections_block(corrections_text)
        if len(questions) != len(corrections):
            raise ValueError("Questions and corrections count mismatch")

        quiz = Quiz(
            slug=source["slug"],
            title=source["title"],
            description=source["description"],
            time_limit_seconds=source["time_limit_seconds"],
        )
        db.add(quiz)
        db.flush()

        for question, correction in zip(questions, corrections):
            correct_index = LETTER_ORDER.index(correction["letter"])
            db.add(
                Question(
                    quiz_id=quiz.id,
                    stem=question["stem"],
                    options=question["options"],
                    correct_index=correct_index,
                    explanation=correction["explanation"],
                )
            )
        imported += 1

    db.commit()
    return {"imported_quizzes": imported}
