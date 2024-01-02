import os
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")

django_asgi = get_asgi_application()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """
    Render the main page using Jinja2 templates.

    :param request: The request object.
    :return: Rendered HTML template of the main page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """
    Retrieve a specific item by its ID.

    :param item_id: The unique identifier of the item.
    :param q: Optional query string.
    :return: A dictionary containing item details.
    """
    return {"item_id": item_id, "q": q}

@app.get("/contacts", response_model=List[Contact])
def get_contacts():
    """
    Get a list of all contacts.

    :return: A list of all contacts in the database.
    """
    return db

@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    """
    Retrieve a specific contact by its ID.

    :param contact_id: The unique identifier of the contact.
    :return: A dictionary containing the contact's details.
    """
    return db[contact_id - 1]

@app.post("/contacts", response_model=Contact)
def create_contact(contact: Contact):
    """
    Create a new contact.

    :param contact: The contact information to be added.
    :return: The newly created contact's information.
    """
    db.append(contact)
    return contact
