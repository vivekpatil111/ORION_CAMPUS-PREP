from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Experience(BaseModel):
    role: str
    company: str
    duration: str
    description: Optional[str] = None

class Education(BaseModel):
    degree: str
    institution: str
    year: str
    field: Optional[str] = None

class AlumniProfile(BaseModel):
    id: str
    user_id: str
    name: str
    email: EmailStr
    current_role: str
    company: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    verified: bool = False
    created_at: datetime

class AlumniCreate(BaseModel):
    name: str
    email: EmailStr
    current_role: str
    company: str
    bio: Optional[str] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None

class MentorshipRequest(BaseModel):
    id: str
    user_id: str
    alumni_id: str
    message: str
    status: str  # pending, accepted, rejected
    created_at: datetime

class MentorshipRequestCreate(BaseModel):
    message: str
