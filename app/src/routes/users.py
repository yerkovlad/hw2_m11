from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, schemas, database, utils
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

router = APIRouter()

limiter = RateLimiter(
    key_func=utils.get_current_user_email,
    rate="1/second",
    block=True,
)

FastAPILimiter.init(limiter)

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(SessionLocal)):
    await rate_limit(request, max_requests=5, interval_seconds=60)
    existing_user = users.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already registered")
    user_data = user.dict()
    user_data["is_verified"] = False  # Додаємо поле для підтвердження електронної пошти
    user_data["verification_token"] = "generate_and_store_unique_verification_token_here"
    send_email(user.email, "Confirm Email", "Please confirm your email.")
    return users.create_user(db, user_data)

@router.get("/verify/{token}", response_model=MessageSchema)
async def verify_email(token: str):
    email = await verify_email_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.email_verified = True
        db.commit()
        return {"message": "Email verification successful."}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/profile", response_model=User)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/avatar", response_model=schemas.User)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(database.get_db)
):
    await FastAPILimiter.check_key(
        limiter,
        utils.get_current_user_email(current_user),
        request=request
    )
    cloudinary_response = upload(file.file)
    avatar_url = cloudinary_url(cloudinary_response['public_id'], format=cloudinary_response['format'])[0]
    db_user = crud.get_user_by_email(db, email=current_user.email)
    if db_user:
        crud.update_user_avatar_url(db, user=db_user, avatar_url=avatar_url)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/reset-password", response_model=schemas.Message)
async def request_reset_password(
    email: str,
    db: Session = Depends(database.get_db)
):
    user = crud.get_user_by_email(db, email=email)
    if user:
        # Generate reset token and send email
        reset_token = utils.generate_reset_token(email)
        await utils.send_reset_password_email(email, reset_token)
        return {"message": "Password reset email sent"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
