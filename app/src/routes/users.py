# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.repository import users
from src.schemas.user import UserCreate, User
from src.utils.security import get_current_user, create_access_token
from src.utils.email import send_email
from src.utils.rate_limiting import rate_limit

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(SessionLocal)):
    await rate_limit(request, max_requests=5, interval_seconds=60)
    existing_user = users.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already registered")
    user_data = user.dict()
    user_data["is_verified"] = False
    user_data["verification_token"] = "generate_and_store_unique_verification_token_here"
    send_email(user.email, "Confirm Email", "Please confirm your email.")
    return users.create_user(db, user_data)
