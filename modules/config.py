"""
Configuration module for Student Review System
Contains all constants, paths, and configuration settings
"""
from pathlib import Path
from typing import Dict, List

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REVIEWS_CSV = DATA_DIR / "student_reviews.csv"
USERS_CSV = DATA_DIR / "users.csv"

# Review categories mapping
CATEGORY_KEYWORDS = {
    "Behavior": [
        "behavior", "disruptive", "cooperative", "polite", "respect",
        "attitude", "classroom demeanor", "follows rules", "tantrums",
        "interrupts", "blurting", "self-control", "sportsmanship"
    ],
    "Homework": [
        "homework", "assignment", "completes", "submitting", "rushes through",
        "written work", "careless errors", "checking work", "editing process"
    ],
    "Participation": [
        "participate", "discussion", "active", "quiet", "contribute",
        "shares ideas", "hand raising", "speaking up", "engaged"
    ],
    "Social Skills": [
        "teamwork", "cooperation", "peers", "classmates", "leadership",
        "helping", "mentor", "dominate", "patient", "empathy", "listening"
    ],
    "Academic Performance": [
        "understanding", "grasp", "ability", "quality", "work", "progress",
        "learning", "concepts", "skills", "achievement"
    ]
}

# Sentiment thresholds
SENTIMENT_THRESHOLDS = {
    "very_positive": 0.6,
    "positive": 0.2,
    "neutral": -0.2,
    "negative": -0.6
}

# User credentials (in production, use proper auth system)
USERS: Dict[str, Dict[str, str]] = {
    "parent1": {"password": "pass1234", "role": "parent", "student_id": "01"},
    "parent2": {"password": "pass1234", "role": "parent", "student_id": "02"},
    "parent3": {"password": "pass1234", "role": "parent", "student_id": "03"},
    "parent4": {"password": "pass1234", "role": "parent", "student_id": "04"},
    "parent5": {"password": "pass1234", "role": "parent", "student_id": "05"},
    "teacher": {"password": "admin1234", "role": "teacher", "student_id": None}
}

# UI Configuration
CHART_COLORS = {
    "positive": "#10B981",  # Green
    "negative": "#EF4444",  # Red
    "neutral": "#6B7280",   # Gray
    "mixed": "#F59E0B"      # Amber
}

# Sentiment descriptors
SENTIMENT_LABELS = {
    "very_positive": "Excellent",
    "positive": "Good",
    "neutral": "Satisfactory",
    "negative": "Needs Improvement",
    "very_negative": "Concerning"
}

# Stop words for text processing (extend as needed)
CUSTOM_STOPWORDS = {"however", "but", "although", "though", "while"}
