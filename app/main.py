from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import contacts
from src.database.db import engine
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
ALGORITHM = os.getenv("")

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
    from src.database.models import Base
    Base.metadata.create_all(bind=engine)

create_tables()
