from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    """
    Pydantic model for JWT access token.

    :param access_token: The JWT access token.
    :param token_type: The type of the token, typically 'bearer'.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Pydantic model for token data.

    :param username: The username extracted from the token, optional.
    """
    username: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.

    :param data: Data to encode in the JWT token.
    :param expires_delta: The timedelta by which the token will expire. If None, defaults to 15 minutes.
    :return: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user from the token.

    :param token: The JWT token.
    :return: TokenData with the username, if successful.
    :raises HTTPException: If token validation fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
