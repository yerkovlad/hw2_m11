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
