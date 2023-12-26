from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, utils
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

limiter = RateLimiter(
    key_func=utils.get_current_user_email,
    rate="1/second",
    block=True,
)

FastAPILimiter.init(limiter)

@router.post("/contacts/", response_model=schemas.Contact)
async def create_contact(
    contact: schemas.ContactCreate,
    current_user: schemas.User = Depends(utils.get_current_user),
    db: Session = Depends(database.get_db)
):
    await FastAPILimiter.check_key(
        limiter, 
        utils.get_current_user_email(current_user), 
        request=request
    )
    
    return crud.create_contact(db, contact, current_user)
