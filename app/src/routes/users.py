from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session
from app import schemas, crud, models, utils, database

router = APIRouter()

@router.post("/register", response_model=MessageSchema)
async def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = utils.get_password_hash(user.password)
    db_user = crud.create_user(db, user, hashed_password)
    
    await utils.send_email_verification(db_user.email)
    
    return {"message": "Registration successful. Check your email for verification."}

@router.get("/verify/{token}", response_model=MessageSchema)
async def verify_email(token: str, db: Session = Depends(database.get_db)):
    email = await utils.verify_email_token(token)

    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        crud.update_user_verification_status(db, user=db_user, is_verified=True)
        return {"message": "Email verification successful."}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/profile", response_model=schemas.User)
async def get_user_profile(current_user: schemas.User = Depends(utils.get_current_user)):
    return current_user
