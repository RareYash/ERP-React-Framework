"""
Chat route — Gemini 2.5 Pro powered teacher assistant.

Uses function-calling so Gemini can dynamically query and modify student data.
"""

import os, json
from typing import Dict, List, Optional
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import google.generativeai as genai

from api.deps import require_teacher
from modules.data_handler import DataHandler
from modules.sentiment_analyzer import SentimentAnalyzer

# ── Load env ────────────────────────────────────────────────────────
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

router = APIRouter(prefix="/api/chat", tags=["chat"])
data_handler = DataHandler()
analyzer = SentimentAnalyzer()

# ── Pydantic schemas ────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str          # "user" or "model"
    text: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    reply: str
    action_taken: Optional[str] = None


# ── Tool functions (called by Gemini) ───────────────────────────────

def _tool_get_student(student_id: str) -> dict:
    """Fetch full details for one student by their ID (e.g. '01')."""
    stu = data_handler.get_student_by_id(student_id)
    if stu is None:
        return {"error": f"Student {student_id} not found."}
    # Attach sentiment
    sentiment = analyzer.analyze_sentiment(stu.get("Teacher Review", ""))
    stu["sentiment"] = sentiment
    # Truncate long review for context efficiency
    review = stu.get("Teacher Review", "")
    if len(review) > 800:
        stu["Teacher Review"] = review[:800] + "…"
    return stu


def _tool_search_students(query: str) -> list:
    """Search students by name or ID fragment."""
    results = data_handler.search_students(query)
    return results[:10]  # cap for token efficiency


def _tool_get_students_by_grade(grade: str) -> list:
    """Get all students in a specific grade."""
    return data_handler.get_students_by_grade(grade)


def _tool_get_class_overview() -> dict:
    """Get a high-level class overview: total students, grade distribution, sentiment breakdown."""
    df = data_handler.load_reviews()
    if df is None or df.empty:
        return {"error": "No data available."}

    students = []
    for _, row in df.iterrows():
        sentiment = analyzer.analyze_sentiment(str(row.get("Teacher Review", "")))
        students.append({
            "id": str(row["Student Number"]).zfill(2),
            "name": row["Student Name"],
            "grade": row["Grade"],
            "archetype": row.get("Archetype", ""),
            "sentiment_label": sentiment["label"],
            "sentiment_score": round(sentiment["compound"], 2),
        })

    # Summary stats
    labels = [s["sentiment_label"] for s in students]
    return {
        "total_students": len(students),
        "sentiment_distribution": {
            "positive": sum(1 for l in labels if "Positive" in l),
            "neutral": sum(1 for l in labels if l == "Neutral"),
            "negative": sum(1 for l in labels if "Negative" in l),
        },
        "grades": list(set(s["grade"] for s in students)),
        "students": students,
    }


def _tool_add_review(student_id: str, review_text: str) -> dict:
    """Add a new review for a student."""
    success = data_handler.add_review(student_id, review_text, "Teacher")
    if success:
        return {"success": True, "message": f"Review added for student {student_id}."}
    return {"success": False, "message": f"Failed to add review for student {student_id}."}


def _tool_get_student_by_name(name: str) -> dict:
    """Find a student by name (case-insensitive)."""
    stu = data_handler.get_student_by_name(name)
    if stu is None:
        return {"error": f"Student '{name}' not found."}
    sentiment = analyzer.analyze_sentiment(stu.get("Teacher Review", ""))
    stu["sentiment"] = sentiment
    review = stu.get("Teacher Review", "")
    if len(review) > 800:
        stu["Teacher Review"] = review[:800] + "…"
    return stu


# Map function names → callables
TOOL_FUNCTIONS = {
    "get_student": _tool_get_student,
    "search_students": _tool_search_students,
    "get_students_by_grade": _tool_get_students_by_grade,
    "get_class_overview": _tool_get_class_overview,
    "add_review": _tool_add_review,
    "get_student_by_name": _tool_get_student_by_name,
}

# ── Gemini tool declarations ────────────────────────────────────────

TOOL_DECLARATIONS = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="get_student",
                description="Get full details for a student by their ID number (e.g. '01', '05', '23'). Returns name, grade, archetype, review text, and sentiment analysis.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "student_id": genai.protos.Schema(type=genai.protos.Type.STRING, description="The student ID number, zero-padded (e.g. '01')"),
                    },
                    required=["student_id"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="get_student_by_name",
                description="Find a student by their name (case-insensitive search). Returns full details including review and sentiment.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "name": genai.protos.Schema(type=genai.protos.Type.STRING, description="Student name to search for"),
                    },
                    required=["name"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="search_students",
                description="Search for students by name or ID fragment. Returns a list of matching students.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "query": genai.protos.Schema(type=genai.protos.Type.STRING, description="Search query text"),
                    },
                    required=["query"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="get_students_by_grade",
                description="Get all students in a specific grade level (e.g. '5th Grade', '8th Grade', 'High School').",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "grade": genai.protos.Schema(type=genai.protos.Type.STRING, description="Grade level, e.g. '5th Grade'"),
                    },
                    required=["grade"],
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="get_class_overview",
                description="Get a complete class overview including all students, their grades, archetypes, and sentiment scores. Use this for broad questions like 'how is the class doing?' or 'who needs attention?'.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={},
                ),
            ),
            genai.protos.FunctionDeclaration(
                name="add_review",
                description="Add a new review comment for a student. The teacher must explicitly ask to add a review.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "student_id": genai.protos.Schema(type=genai.protos.Type.STRING, description="Student ID (e.g. '01')"),
                        "review_text": genai.protos.Schema(type=genai.protos.Type.STRING, description="The review text to add"),
                    },
                    required=["student_id", "review_text"],
                ),
            ),
        ]
    )
]


# ── System prompt ───────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an AI teaching assistant for the Student Review System.
You help teachers manage and understand their student data.

IMPORTANT RULES:
1. You can ONLY discuss topics related to the students, their reviews, grades, archetypes, and sentiments in this system.
2. If asked about anything unrelated to the student data or the school system, politely decline and redirect to student-related topics.
3. Use the provided tools to fetch real-time data. NEVER make up student information.
4. When the teacher asks about a student, use get_student or get_student_by_name to look them up.
5. For broad class questions, use get_class_overview.
6. Only use add_review when the teacher EXPLICITLY asks to add a review. Confirm the action after doing it.
7. Be concise, friendly, and professional. Use emojis sparingly to keep it engaging.
8. When presenting student data, format it nicely with names, IDs, and scores.
9. If sentiment is negative, phrase it supportively (e.g., "needs attention" rather than "doing badly").

STUDENT DATA SCHEMA:
- Student Number: zero-padded ID (01-50)
- Student Name: full name
- Grade: e.g. "5th Grade", "8th Grade", "High School"
- Subject: e.g. "General", "Math", "Science"
- Archetype: teacher-assigned label like "Creative Explorer", "The Natural Leader"
- Teacher Review: text containing original review + timestamped additions
- Sentiment: analyzed from review text (Very Positive / Positive / Neutral / Negative / Very Negative)
"""


# ── Chat endpoint ───────────────────────────────────────────────────

@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current_user: Dict = Depends(require_teacher),
):
    """Process a chat message using Gemini with function calling."""
    # Logic check:
    # 1. GEMINI_KEY must exist
    # 2. GEMINI_KEY must NOT be the placeholder "your_api_key_here"
    if not GEMINI_KEY or GEMINI_KEY == "your_api_key_here":
        raise HTTPException(status_code=500, detail="Gemini API key not configured. Set GEMINI_API_KEY in .env")

    genai.configure(api_key=GEMINI_KEY)

    # Use the latest Flash model
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        tools=TOOL_DECLARATIONS,
        system_instruction=SYSTEM_PROMPT,
    )

    # Build conversation history for Gemini
    gemini_history = []
    for msg in body.history:
        gemini_history.append(
            genai.protos.Content(
                role=msg.role if msg.role == "user" else "model",
                parts=[genai.protos.Part(text=msg.text)],
            )
        )

    chat_session = model.start_chat(history=gemini_history)

    action_taken = None

    try:
        response = chat_session.send_message(body.message)

        # Handle function calling loop (Gemini may call multiple tools)
        max_iterations = 5
        iteration = 0
        while response.candidates[0].content.parts[0].function_call.name and iteration < max_iterations:
            iteration += 1
            fn_call = response.candidates[0].content.parts[0].function_call
            fn_name = fn_call.name
            fn_args = dict(fn_call.args) if fn_call.args else {}

            # Execute the tool
            tool_fn = TOOL_FUNCTIONS.get(fn_name)
            if tool_fn is None:
                result = {"error": f"Unknown function: {fn_name}"}
            else:
                try:
                    result = tool_fn(**fn_args)
                    if fn_name == "add_review":
                        action_taken = f"Added review for student {fn_args.get('student_id', '?')}"
                except Exception as e:
                    result = {"error": str(e)}

            # Send function result back to Gemini
            response = chat_session.send_message(
                genai.protos.Content(
                    parts=[
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn_name,
                                response={"result": json.dumps(result, default=str)},
                            )
                        )
                    ]
                )
            )

        # Extract text response
        reply_text = response.text if response.text else "I'm sorry, I couldn't generate a response."

    except Exception as e:
        reply_text = f"Sorry, I encountered an error: {str(e)}"

    return ChatResponse(reply=reply_text, action_taken=action_taken)
