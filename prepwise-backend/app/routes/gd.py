from fastapi import APIRouter, HTTPException, Depends, Header, Query
from typing import Optional, Dict, List, Any
import uuid
from datetime import datetime
import firebase_admin.auth

from app.services.firebase_service import FirebaseService
from app.services.gemini_service import GeminiService
from app.services.gd_service import GDService

router = APIRouter(prefix="/gd", tags=["gd"])

firebase_service = FirebaseService()
gemini_service = GeminiService()
gd_service = GDService()

# In-memory active GD sessions
active_gd_sessions = {}


def verify_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return "user_123"
    try:
        token = authorization.replace("Bearer ", "")
        decoded = firebase_admin.auth.verify_id_token(token)
        return decoded.get("uid", "user_123")
    except Exception:
        return "user_123"


@router.post("/start")
async def start_gd(
    mode: str = Query(..., description="Interview mode (text/voice/video)"),
    user_id: str = Depends(verify_user)
):
    """Start a new Group Discussion session"""
    """Start a new Group Discussion session"""
    try:
        gd_id = str(uuid.uuid4())
        
        # Generate GD topic dynamically
        topic = await gd_service.generate_topic()
        
        # Initialize AI participants with fixed personalities
        ai_participants = gd_service.create_ai_participants()
        
        # Initialize behavior tracking
        behavior_tracking = {
            "student_speaks_count": 0,
            "student_initiated": False,
            "student_interruptions": 0,
            "student_interrupted_count": 0,
            "student_summarized": False,
            "student_concluded": False,
            "conversation_history": [],
            "turn_order": []
        }
        
        active_gd_sessions[gd_id] = {
            "user_id": user_id,
            "mode": mode,
            "topic": topic,
            "ai_participants": ai_participants,
            "behavior_tracking": behavior_tracking,
            "started_at": datetime.utcnow(),
            "status": "active",
            "current_speaker": None,
            "turn_count": 0
        }
        
        # Save to Firestore
        firebase_service.create_interview(gd_id, {
            "user_id": user_id,
            "interview_type": "gd",
            "mode": mode,
            "status": "in_progress",
            "topic": topic,
            "created_at": datetime.utcnow()
        })
        
        return {
            "gd_id": gd_id,
            "topic": topic,
            "ai_participants": ai_participants,
            "first_message": None  # No auto-start, wait for student
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{gd_id}/speak")
async def student_speak(
    gd_id: str,
    message: str = Query(..., description="Student's message"),
    interrupted: bool = Query(False, description="Whether student interrupted"),
    user_id: str = Depends(verify_user)
):
    """Student speaks in the GD"""
    """Student speaks in the GD"""
    try:
        session = active_gd_sessions.get(gd_id)
        if not session:
            raise HTTPException(status_code=404, detail="GD session not found")
        
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        # Update behavior tracking
        tracking = session["behavior_tracking"]
        tracking["student_speaks_count"] += 1
        if interrupted:
            tracking["student_interruptions"] += 1
        if tracking["turn_count"] == 0:
            tracking["student_initiated"] = True
        
        # Add student message to history
        tracking["conversation_history"].append({
            "speaker": "student",
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "interrupted": interrupted
        })
        tracking["turn_order"].append("student")
        session["turn_count"] += 1
        
        # Get AI response(s) - multiple AI participants may react
        ai_responses = await gd_service.get_ai_responses(
            topic=session["topic"],
            conversation_history=tracking["conversation_history"],
            ai_participants=session["ai_participants"],
            student_message=message
        )
        
        # Add AI responses to history
        for response in ai_responses:
            tracking["conversation_history"].append(response)
            tracking["turn_order"].append(response["speaker"])
        
        session["turn_count"] += len(ai_responses)
        
        return {
            "gd_id": gd_id,
            "student_message": message,
            "ai_responses": ai_responses,
            "turn_count": session["turn_count"],
            "behavior_tracking": tracking
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{gd_id}/end")
async def end_gd(
    gd_id: str,
    user_id: str = Depends(verify_user)
):
    """End the GD and generate evaluation"""
    try:
        session = active_gd_sessions.get(gd_id)
        if not session:
            raise HTTPException(status_code=404, detail="GD session not found")
        
        if session["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        # Generate behavior-based evaluation
        evaluation = await gd_service.evaluate_gd_performance(
            topic=session["topic"],
            conversation_history=session["behavior_tracking"]["conversation_history"],
            behavior_tracking=session["behavior_tracking"]
        )
        
        results = {
            "gd_id": gd_id,
            "user_id": user_id,
            "topic": session["topic"],
            "mode": session["mode"],
            "overall_score": evaluation["overall_score"],
            "scores": evaluation["scores"],
            "strengths": evaluation["strengths"],
            "weaknesses": evaluation["weaknesses"],
            "role_suitability": evaluation["role_suitability"],
            "improvement_suggestions": evaluation["improvement_suggestions"],
            "behavior_summary": session["behavior_tracking"],
            "detailed_feedback": evaluation["detailed_feedback"],
            "created_at": session["started_at"],
            "completed_at": datetime.utcnow()
        }
        
        # Save to Firestore
        firebase_service.update_interview(gd_id, {
            "status": "completed",
            "completed_at": datetime.utcnow(),
            "results": results
        })
        
        del active_gd_sessions[gd_id]
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{gd_id}/status")
async def get_gd_status(
    gd_id: str,
    user_id: str = Depends(verify_user)
):
    """Get current GD session status"""
    session = active_gd_sessions.get(gd_id)
    if not session:
        raise HTTPException(status_code=404, detail="GD session not found")
    
    if session["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return {
        "gd_id": gd_id,
        "topic": session["topic"],
        "turn_count": session["turn_count"],
        "status": session["status"],
        "behavior_tracking": session["behavior_tracking"],
        "recent_messages": session["behavior_tracking"]["conversation_history"][-10:]
    }

