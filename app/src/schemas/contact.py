from typing import List
from pydantic import BaseModel
from datetime import datetime

class ContactBase(BaseModel):
    """
    Base Pydantic model for contact data.

    :param first_name: The first name of the contact.
    :param last_name: The last name of the contact.
    :param email: The email of the contact.
    :param phone_number: The phone number of the contact.
    :param birthday: The birthday of the contact.
    :param additional_data: Additional data for the contact (optional).
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime
    additional_data: str = None

class ContactCreate(ContactBase):
    """
    Pydantic model for creating a new contact.

    Inherits from ContactBase.
    """
    pass

class ContactUpdate(ContactBase):
    """
    Pydantic model for updating an existing contact.

    Inherits from ContactBase.
    """
    pass

class Contact(ContactBase):
    """
    Pydantic model for displaying contact details.

    Inherits from ContactBase and includes an additional 'id' field.

    :param id: The unique identifier for the contact.
    """
    id: int

    class Config:
        orm_mode = True

class ContactSearch(ContactBase):
    """
    Pydantic model for searching contacts.

    Inherits from ContactBase.
    """
    pass

class ContactList(BaseModel):
    """
    Pydantic model for displaying a list of contacts.

    :param contacts: List of Contact models.
    """
    contacts: List[Contact]
