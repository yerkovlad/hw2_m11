from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.

    :param email: Email of the user.
    :param password: Password of the user.
    :param name: Name of the user, optional.
    """
    email: EmailStr
    password: str
    name: str = Field(None, title="Name of the User")

class UserDisplay(BaseModel):
    """
    Pydantic model for displaying user data.

    :param id: Unique identifier for the user.
    :param email: Email of the user.
    :param name: Name of the user, optional.
    """
    id: int
    email: EmailStr
    name: str = Field(None, title="Name of the User")

    class Config:
        orm_mode = True

class PasswordResetRequest(BaseModel):
    """
    Pydantic model for requesting a password reset.

    :param email: Email of the user requesting the password reset.
    """
    email: EmailStr

class PasswordReset(BaseModel):
    """
    Pydantic model for resetting the user's password.

    :param token: Token for password reset.
    :param new_password: New password for the user.
    """
    token: str
    new_password: str
