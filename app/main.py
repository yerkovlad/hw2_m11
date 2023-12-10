from fastapi import FastAPI
from src.routes import contacts
from src.database.db import engine

app = FastAPI()

# Include routes
app.include_router(contacts.router)

# Create the database tables
def create_tables():
    from src.database.models import Base
    Base.metadata.create_all(bind=engine)

create_tables()
