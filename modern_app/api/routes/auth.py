"""
Auth Routes — Login endpoint with rate limiting.
"""
import hmac
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

# --- Import existing auth module by adding project root to path ---
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.config import USERS
from api.deps import create_access_token

# -------------------------------------------------------------------
# Router & rate limiter
# -------------------------------------------------------------------
router = APIRouter(prefix="/api/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


# -------------------------------------------------------------------
# Request / Response schemas
# -------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    student_id: str | None = None


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
def login(request: Request, body: LoginRequest):
    """
    Authenticate a user and return a JWT.

    Rate limited to 10 attempts per minute per IP.
    """
    user: Dict[str, Any] | None = USERS.get(body.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Constant-time password comparison to prevent timing attacks
    if not hmac.compare_digest(user["password"], body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        data={
            "sub": body.username,
            "role": user["role"],
            "student_id": user.get("student_id"),
        }
    )

    return LoginResponse(
        access_token=token,
        role=user["role"],
        username=body.username,
        student_id=user.get("student_id"),
    )
