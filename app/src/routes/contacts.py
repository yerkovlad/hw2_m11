from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db import SessionLocal, engine
from src.repository import contacts
from src.schemas.contact import ContactCreate, ContactUpdate, ContactList

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contacts/", response_model=ContactList)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contacts.create_contact(db, contact)

@router.get("/contacts/", response_model=ContactList)
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return contacts.get_contacts(db, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=ContactList)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return contacts.get_contact(db, contact_id)

@router.put("/contacts/{contact_id}", response_model=ContactList)
def update_existing_contact(contact_id: int, update_data: ContactUpdate, db: Session = Depends(get_db)):
    return contacts.update_contact(db, contact_id, update_data.dict())

@router.delete("/contacts/{contact_id}", response_model=ContactList)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    return contacts.delete_contact(db, contact_id)
