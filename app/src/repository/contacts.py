from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas.contact import ContactCreate
from src.schemas.token import create_access_token
from src.database.db import password_hasher

def register_user(db: Session, contact: ContactCreate):
    """
    Register a new user in the database.

    :param db: The database session.
    :param contact: The contact information for the new user.
    :return: The created user object.
    """
    db_contact = Contact(**contact.dict(), hashed_password=password_hasher.create_password_hash(contact.password))
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user based on email and password.

    :param db: The database session.
    :param email: The email of the user.
    :param password: The password of the user.
    :return: The authenticated user or None if authentication fails.
    """
    user = db.query(Contact).filter(Contact.email == email).first()
    if user and password_hasher.verify_password(password, user.hashed_password):
        return user
    return None

def create_access_token_data(user: Contact):
    """
    Create access token data for a user.

    :param user: The user object for which the access token is created.
    :return: A dictionary containing the access token data.
    """
    return {"sub": user.email}
