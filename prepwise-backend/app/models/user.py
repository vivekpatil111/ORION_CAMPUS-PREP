from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    user_id: str
    email: EmailStr
    name: Optional[str] = None
    created_at: datetime
    role: Optional[str] = "user"  # user, admin

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
