from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas.contact import ContactCreate
from src.schemas.token import create_access_token
from src.database.db import password_hasher

def register_user(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict(), hashed_password=password_hasher.create_password_hash(contact.password))
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Contact).filter(Contact.email == email).first()
    if user and password_hasher.verify_password(password, user.hashed_password):
        return user
    return None

def create_access_token_data(user: Contact):
    return {"sub": user.email}
