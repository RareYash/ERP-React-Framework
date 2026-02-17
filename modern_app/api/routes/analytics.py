"""
Analytics Routes — Class-wide and grade-wise analytics (teacher only).
"""
from typing import Dict, Any, List

from fastapi import APIRouter, Depends

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.data_handler import DataHandler
from modules.summarizer import ReviewSummarizer
from modules.sentiment_analyzer import SentimentAnalyzer
from api.deps import require_teacher

# -------------------------------------------------------------------
router = APIRouter(prefix="/api/analytics", tags=["analytics"])

data_handler = DataHandler()
summarizer = ReviewSummarizer()
analyzer = SentimentAnalyzer()


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@router.get("/class")
def class_analytics(current_user: Dict = Depends(require_teacher)):
    """
    Get class-wide analytics:
    - Sentiment distribution across all students
    - Archetype breakdown
    """
    df = data_handler.load_reviews()
    records = df.to_dict("records")

    sentiments = []
    for record in records:
        review = record.get("Teacher Review", "")
        result = analyzer.analyze_sentiment(review)
        sentiments.append(
            {
                "student_id": record.get("Student Number"),
                "student_name": record.get("Student Name"),
                "grade": record.get("Grade"),
                "archetype": record.get("Archetype"),
                "compound": result["compound"],
                "label": result["label"],
            }
        )

    # Archetype counts
    archetype_counts: Dict[str, int] = {}
    for s in sentiments:
        arch = s.get("archetype", "Unknown")
        archetype_counts[arch] = archetype_counts.get(arch, 0) + 1

    # Sentiment distribution
    label_counts: Dict[str, int] = {}
    for s in sentiments:
        lbl = s["label"]
        label_counts[lbl] = label_counts.get(lbl, 0) + 1

    return {
        "students": sentiments,
        "student_sentiments": [
            {
                "id": s["student_id"],
                "name": s["student_name"],
                "compound": s["compound"],
                "label": s["label"],
            }
            for s in sentiments
        ],
        "archetype_counts": archetype_counts,
        "label_counts": label_counts,
        "total_students": len(sentiments),
    }


@router.get("/grades")
def grade_analytics(current_user: Dict = Depends(require_teacher)):
    """Grade-wise sentiment comparison."""
    grades = data_handler.get_unique_grades()
    result = []

    for grade in grades:
        students = data_handler.get_students_by_grade(grade)
        comparison = summarizer.compare_students(students)
        result.append(
            {
                "grade": grade,
                "avg_sentiment": comparison["average_sentiment"],
                "student_count": comparison["student_count"],
                "category_averages": comparison.get("category_averages", {}),
            }
        )

    return result


@router.get("/filters")
def get_filters(current_user: Dict = Depends(require_teacher)):
    """Get available filter options (grades and archetypes)."""
    return {
        "grades": data_handler.get_unique_grades(),
        "archetypes": data_handler.get_unique_archetypes(),
    }
