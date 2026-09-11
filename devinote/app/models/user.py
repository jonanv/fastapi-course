from pydantic import ConfigDict, EmailStr
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    full_name: str = Field(default="")
    hashed_password: str
    is_active: bool = Field(default=True)

class UserCreate(SQLModel):
    email: EmailStr
    full_name: str = ""
    password: str

class UserRead(SQLModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)