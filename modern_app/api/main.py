"""
Student Review System — FastAPI Backend
Main application entry point.

Start with:
    cd api && uvicorn main:app --reload --port 8000
"""
import sys
from pathlib import Path

# Ensure the project root is on sys.path so `modules.*` imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.routes.auth import router as auth_router
from api.routes.students import router as students_router
from api.routes.analytics import router as analytics_router
from api.routes.chat import router as chat_router

# -------------------------------------------------------------------
# App setup
# -------------------------------------------------------------------
app = FastAPI(
    title="Student Review System API",
    version="2.0.0",
    description="REST API for the Student Review System — sentiment analysis of teacher reviews.",
)

# -------------------------------------------------------------------
# Rate limiter (shared instance used by route decorators)
# -------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -------------------------------------------------------------------
# CORS — restrict to the React dev server and production origin
# -------------------------------------------------------------------

ALLOWED_ORIGINS = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# Security headers middleware
# -------------------------------------------------------------------
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# -------------------------------------------------------------------
# Mount routers
# -------------------------------------------------------------------
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(analytics_router)
app.include_router(chat_router)


# -------------------------------------------------------------------
# Health check
# -------------------------------------------------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
