"""
Student Routes — CRUD operations on student data with ownership checks.
"""
import re
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.data_handler import DataHandler
from modules.summarizer import ReviewSummarizer
from modules.sentiment_analyzer import SentimentAnalyzer
from api.deps import get_current_user, require_teacher

# -------------------------------------------------------------------
# Router
# -------------------------------------------------------------------
router = APIRouter(prefix="/api/students", tags=["students"])

# Shared instances (created once, reused across requests)
data_handler = DataHandler()
summarizer = ReviewSummarizer()
analyzer = SentimentAnalyzer()


# -------------------------------------------------------------------
# Schemas
# -------------------------------------------------------------------
class StudentBrief(BaseModel):
    id: str
    name: str


class ReviewAddRequest(BaseModel):
    review_text: str
    teacher_name: str = "Teacher"


class ReviewUpdateRequest(BaseModel):
    review_text: str


class SentimentPreview(BaseModel):
    compound: float
    label: str
    raw_score: float
    has_contrast: bool = False


class StudentDetailsUpdate(BaseModel):
    name: str | None = None
    grade: str | None = None
    archetype: str | None = None


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def _enforce_ownership(current_user: Dict[str, Any], student_id: str):
    """
    Parents may only access their own child's data.
    Teachers have access to all students.
    """
    if current_user["role"] == "parent":
        if current_user.get("student_id") != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own child's data",
            )


def _parse_individual_reviews(full_review: str) -> list[dict]:
    """
    Parse the concatenated review text into individual review entries.

    Reviews are stored as:
        Original review text

        [2026-02-11 - Teacher]: subsequent review
    """
    if not full_review or not full_review.strip():
        return []

    # Pattern: [date - teacher]: review text
    pattern = r'\[(\d{4}-\d{2}-\d{2})\s*-\s*([^\]]+)\]:\s*'
    parts = re.split(pattern, full_review)

    reviews = []

    # First chunk (before any [date - teacher]:) is the original review
    if parts[0].strip():
        reviews.append({
            "date": "Original",
            "teacher": "Original",
            "text": parts[0].strip(),
        })

    # Subsequent chunks come in groups of 3: date, teacher, text
    i = 1
    while i + 2 <= len(parts):
        date = parts[i]
        teacher = parts[i + 1].strip()
        text = parts[i + 2].strip() if i + 2 < len(parts) else ""
        if text:
            reviews.append({"date": date, "teacher": teacher, "text": text})
        i += 3

    return reviews


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@router.get("/", response_model=List[StudentBrief])
def list_students(current_user: Dict = Depends(get_current_user)):
    """
    List all students (teachers see all; parents see only their child).
    """
    all_students = data_handler.get_all_students()

    if current_user["role"] == "parent":
        parent_sid = current_user.get("student_id")
        return [s for s in all_students if s["id"] == parent_sid]

    return all_students


@router.get("/{student_id}")
def get_student(student_id: str, current_user: Dict = Depends(get_current_user)):
    """Get full student record by ID (with ownership check)."""
    _enforce_ownership(current_user, student_id)

    student = data_handler.get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.get("/{student_id}/summary")
def get_student_summary(
    student_id: str, current_user: Dict = Depends(get_current_user)
):
    """Get sentiment summary for a student (with ownership check)."""
    _enforce_ownership(current_user, student_id)

    student = data_handler.get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    summary = summarizer.generate_summary(student)
    return summary


@router.get("/{student_id}/reviews")
def get_individual_reviews(
    student_id: str, current_user: Dict = Depends(get_current_user)
):
    """
    Parse individual reviews with per-review sentiment scores
    and a collective final score.
    """
    _enforce_ownership(current_user, student_id)

    student = data_handler.get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    full_review = student.get("Teacher Review", "")
    individual_reviews = _parse_individual_reviews(full_review)

    # Score each individual review
    scored_reviews = []
    scores = []
    for rev in individual_reviews:
        sentiment = analyzer.analyze_sentiment(rev["text"])
        scored_reviews.append({
            **rev,
            "sentiment": {
                "compound": sentiment["compound"],
                "label": sentiment["label"],
                "raw_score": sentiment.get("raw_score", sentiment["compound"]),
            },
        })
        scores.append(sentiment["compound"])

    # Calculate collective final score (average of individual scores)
    if scores:
        final_compound = sum(scores) / len(scores)
    else:
        final_compound = 0.0

    final_label = analyzer._get_sentiment_label(final_compound)

    return {
        "reviews": scored_reviews,
        "final_score": {
            "compound": round(final_compound, 4),
            "label": final_label,
            "total_reviews": len(scored_reviews),
        },
    }


@router.post("/{student_id}/review")
def add_review(
    student_id: str,
    body: ReviewAddRequest,
    current_user: Dict = Depends(require_teacher),
):
    """Add a review for a student (teacher only)."""
    success = data_handler.add_review(
        student_id=student_id,
        review_text=body.review_text,
        teacher_name=body.teacher_name,
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add review")

    return {"message": "Review added successfully"}


@router.put("/{student_id}/review")
def update_review(
    student_id: str,
    body: ReviewUpdateRequest,
    current_user: Dict = Depends(require_teacher),
):
    """Replace entire review for a student (teacher only)."""
    success = data_handler.update_review(
        student_id=student_id, new_review=body.review_text
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update review")

    return {"message": "Review updated successfully"}


@router.put("/{student_id}/details")
def update_student_details(
    student_id: str,
    body: StudentDetailsUpdate,
    current_user: Dict = Depends(require_teacher),
):
    """Edit student details — name, grade, archetype (teacher only)."""
    success = data_handler.update_student_details(
        student_id=student_id,
        name=body.name,
        grade=body.grade,
        archetype=body.archetype,
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update student details")

    return {"message": "Student details updated successfully"}


@router.get("/search/{query}")
def search_students(query: str, current_user: Dict = Depends(get_current_user)):
    """Search students by name or ID."""
    results = data_handler.search_students(query)

    # Parents can only see their own child in results
    if current_user["role"] == "parent":
        parent_sid = current_user.get("student_id")
        results = [r for r in results if r.get("Student Number") == parent_sid]

    return results


@router.post("/sentiment-preview", response_model=SentimentPreview)
def sentiment_preview(
    body: ReviewAddRequest,
    current_user: Dict = Depends(require_teacher),
):
    """Live sentiment preview for a review being written (teacher only)."""
    result = analyzer.analyze_sentiment(body.review_text)
    return SentimentPreview(
        compound=result["compound"],
        label=result["label"],
        raw_score=result.get("raw_score", result["compound"]),
        has_contrast=result.get("has_contrast", False),
    )
