from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum


class InterviewType(str, Enum):
    HR = "hr"
    TECHNICAL = "technical"
    GD = "gd"


class InterviewMode(str, Enum):
    TEXT = "text"
    VOICE = "voice"
    VIDEO = "video"


class InterviewStart(BaseModel):
    interview_type: InterviewType
    mode: InterviewMode
    resume_data: Optional[Dict[str, Any]] = None


class InterviewResponse(BaseModel):
    interview_id: str
    current_question: str
    question_number: int
    is_finished: bool


class AnswerSubmit(BaseModel):
    answer: str
    interview_id: str


class InterviewResult(BaseModel):
    interview_id: str
    user_id: str
    interview_type: str
    mode: str
    overall_score: float
    scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    detailed_feedback: str
    created_at: str
