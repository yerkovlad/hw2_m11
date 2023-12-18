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

@router.post("/contacts/", response_model=ContactList)
def create_new_contact(contact: ContactCreate, db: Session = Depends(db.get_db), current_user: Contact = Depends(get_current_user)):
    return contacts.create_contact(db, contact, current_user.id)

@router.get("/contacts/", response_model=ContactList)
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db), current_user: Contact = Depends(get_current_user)):
    return contacts.get_contacts(db, skip=skip, limit=limit, user_id=current_user.id)

@router.get("/contacts/{contact_id}", response_model=ContactList)
def read_contact(contact_id: int, db: Session = Depends(db.get_db), current_user: Contact = Depends(get_current_user)):
    return contacts.get_contact(db, contact_id, user_id=current_user.id)

@router.put("/contacts/{contact_id}", response_model=ContactList)
def update_existing_contact(contact_id: int, update_data: ContactUpdate, db: Session = Depends(db.get_db), current_user: Contact = Depends(get_current_user)):
    return contacts.update_contact(db, contact_id, update_data.dict(), user_id=current_user.id)

@router.delete("/contacts/{contact_id}", response_model=ContactList)
def delete_existing_contact(contact_id: int, db: Session = Depends(db.get_db), current_user: Contact = Depends(get_current_user)):
    return contacts.delete_contact(db, contact_id, user_id=current_user.id)
