from typing import List
from pydantic import BaseModel
from datetime import datetime

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: datetime
    additional_data: str = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class ContactSearch(ContactBase):
    pass

class ContactList(BaseModel):
    contacts: List[Contact]
