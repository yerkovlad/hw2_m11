# src/routes/contacts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import db
from src.repository import contacts
from src.schemas.contact import ContactCreate, ContactUpdate, ContactList
from src.schemas.token import Token, create_access_token, get_current_user

router = APIRouter()

@router.post("/register/", response_model=Token)
def register_user(contact: ContactCreate, db: Session = Depends(db.get_db)):
    existing_user = db.query(Contact).filter(Contact.email == contact.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    user = contacts.register_user(db, contact)
    access_token = create_access_token(data=create_access_token_data(user))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token/", response_model=Token)
def login_for_access_token(contact: ContactCreate, db: Session = Depends(db.get_db)):
    user = contacts.authenticate_user(db, contact.email, contact.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data=create_access_token_data(user))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=ContactList)
def read_user_me(current_user: Contact = Depends(get_current_user), db: Session = Depends(db.get_db)):
    return contacts.get_contact(db, current_user.id)
