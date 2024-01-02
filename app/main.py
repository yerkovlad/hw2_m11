from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import contacts
from src.database.db import engine
import os
from app.settings import *
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_django_project.settings')

app.include_router(contacts.router)
app.include_router(users.router, prefix="/users")

django_app = get_asgi_application()

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)

def create_tables():
    """
    Create a new tables.

    :return: None
    """
    from src.database.models import Base
    Base.metadata.create_all(bind=engine)

create_tables()
