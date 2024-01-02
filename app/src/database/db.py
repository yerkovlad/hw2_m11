from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = "postgresql://yerkovlad:02012009@localhost/yerv"
SECRET_KEY = "secretkey"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()
metadata = Base.metadata

class Database:
    def __init__(self):
        """Initialize a new Database instance."""
        self.db = SessionLocal()

    def get_db(self):
        """
        Get the current database session.

        :return: sqlalchemy.orm.Session, The current database session.
        """
        return self.db

db = Database()

class PasswordHasher:
    def __init__(self, rounds: int = 12):
        """
        Initialize a new PasswordHasher instance.

        :param rounds: The number of hashing rounds. Defaults to 12.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", rounds=rounds)

    def create_password_hash(self, password: str):
        """
        Create a hashed version of the given password.

        :param password: The plain-text password.
        :return: str, The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        """
        Verify a plain-text password against its hashed version.

        :param plain_password: The plain-text password.
        :param hashed_password: The hashed password to compare against.
        :return: bool, True if the passwords match, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

password_hasher = PasswordHasher()
