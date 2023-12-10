from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import database, SessionLocal
from app.models.contact import Contact, ContactCreate, ContactUpdate, ContactSearch, ContactList, upcoming_birthdays, search_contacts, create_contact, get_contacts, get_contact, update_contact, delete_contact

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=Contact)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)

@app.get("/contacts/", response_model=ContactList)
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_contacts(db, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return get_contact(db, contact_id)

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_existing_contact(contact_id: int, update_data: ContactUpdate, db: Session = Depends(get_db)):
    return update_contact(db, contact_id, update_data.dict())

@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    return delete_contact(db, contact_id)

@app.get("/contacts/search/", res
