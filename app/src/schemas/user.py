from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str = Field(None, title="Name of the User")

class UserDisplay(BaseModel):
    id: int
    email: EmailStr
    name: str = Field(None, title="Name of the User")

    class Config:
        orm_mode = True

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str
