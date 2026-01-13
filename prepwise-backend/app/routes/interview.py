from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Header
from typing import Optional
import uuid
from datetime import datetime
import firebase_admin.auth

# Import models directly from model file (not from app.models to avoid circular imports)
from app.models.interview import InterviewStart, InterviewResponse
from app.services.firebase_service import FirebaseService
from app.services.gemini_service import GeminiService
from app.services.voice_emotion import VoiceEmotionService
from app.services.video_analysis import VideoAnalysisService
from app.utils.video_processing import extract_frames

# #region agent log
import json
import os
log_path = r"c:\Users\shlok\OneDrive\Desktop\prepwise_interview\.cursor\debug.log"
def log_debug(location, message, data=None, hypothesis_id="A"):
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "location": location,
                "message": message,
                "data": data or {},
                "timestamp": datetime.utcnow().isoformat(),
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": hypothesis_id
            }) + "\n")
    except:
        pass
# #endregion

router = APIRouter(prefix="/interview", tags=["interview"])

# Services
firebase_service = FirebaseService()
gemini_service = GeminiService()
voice_service = VoiceEmotionService()
video_service = VideoAnalysisService()

# In-memory active interviews
active_interviews = {}


# ---------------- AUTH ----------------
def verify_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return "user_123"  # dev fallback

    try:
        token = authorization.replace("Bearer ", "")
        decoded = firebase_admin.auth.verify_id_token(token)
        return decoded.get("uid", "user_123")
    except Exception:
        return "user_123"


# ---------------- START INTERVIEW ----------------
@router.post("/start", response_model=InterviewResponse)
async def start_interview(
    interview_data: InterviewStart,
    user_id: str = Depends(verify_user)
):
    # #region agent log
    log_debug("interview.py:start_interview:entry", "Interview start called", {
        "interview_type": interview_data.interview_type.value if interview_data.interview_type else None,
        "mode": interview_data.mode.value if interview_data.mode else None,
        "user_id": user_id
    }, "A")
    # #endregion
    
    try:
        interview_id = str(uuid.uuid4())
        
        # #region agent log
        log_debug("interview.py:start_interview:after_id", "Interview ID generated", {"interview_id": interview_id}, "A")
        # #endregion

        first_question = await gemini_service.generate_question(
            interview_type=interview_data.interview_type.value,
            question_number=1,
            resume_data=interview_data.resume_data
        )

        if not first_question:
            first_question = "Tell me about yourself."

        active_interviews[interview_id] = {
            "user_id": user_id,
            "interview_type": interview_data.interview_type.value,
            "mode": interview_data.mode.value,
            "questions": [first_question],
            "answers": [],
            "qa_pairs": [],
            "resume_data": interview_data.resume_data,
            "started_at": datetime.utcnow(),
            "emotion_analyses": [],
            "video_analyses": []
        }

        firebase_service.create_interview(interview_id, {
            "user_id": user_id,
            "interview_type": interview_data.interview_type.value,
            "mode": interview_data.mode.value,
            "status": "in_progress",
            "created_at": datetime.utcnow()
        })

        return InterviewResponse(
            interview_id=interview_id,
            current_question=first_question,
            question_number=1,
            is_finished=False
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- SUBMIT ANSWER ----------------
@router.post("/{interview_id}/answer")
async def submit_answer(
    interview_id: str,
    answer: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    user_id: str = Depends(verify_user)
):
    try:
        interview = active_interviews.get(interview_id)

        if not interview:
            raise HTTPException(status_code=404, detail="Interview not active")

        if interview["user_id"] != user_id and user_id != "user_123":
            raise HTTPException(status_code=403, detail="Unauthorized")

        text_answer = answer or ""

        # ---------- AUDIO ----------
        if audio:
            audio_bytes = await audio.read()
            voice_data = voice_service.get_comprehensive_analysis(audio_bytes)
            text_answer = voice_data.get("transcription", text_answer)
            if voice_data.get("emotions"):
                interview["emotion_analyses"].append(voice_data["emotions"])

        # ---------- VIDEO ----------
        if video:
            video_bytes = await video.read()
            frames = extract_frames(video_bytes)
            video_data = video_service.analyze_video(frames)
            if video_data:
                interview["video_analyses"].append(video_data)

        current_question = interview["questions"][-1]

        interview["answers"].append(text_answer)
        interview["qa_pairs"].append({
            "question": current_question,
            "answer": text_answer
        })

        question_number = len(interview["questions"])
        is_finished = question_number >= 5

        next_question = ""

        if not is_finished:
            next_question = await gemini_service.generate_question(
                interview_type=interview["interview_type"],
                question_number=question_number + 1,
                previous_answers=interview["answers"],
                resume_data=interview["resume_data"]
            )
            interview["questions"].append(next_question)

        firebase_service.update_interview(
            interview_id,
            {
                "questions": interview["questions"],
                "answers": interview["answers"],
                "qa_pairs": interview["qa_pairs"],
                "last_updated": datetime.utcnow()
            }
        )

        return {
            "interview_id": interview_id,
            "current_question": next_question if not is_finished else "",
            "question_number": question_number,
            "is_finished": is_finished,
            "transcribed_text": text_answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- END INTERVIEW ----------------
@router.post("/{interview_id}/end")
async def end_interview(
    interview_id: str,
    user_id: str = Depends(verify_user)
):
    try:
        interview = active_interviews.get(interview_id)

        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")

        if interview["user_id"] != user_id and user_id != "user_123":
            raise HTTPException(status_code=403, detail="Unauthorized")

        feedback = await gemini_service.generate_final_feedback(
            interview_type=interview["interview_type"],
            all_qa_pairs=interview["qa_pairs"],
            emotion_analysis=None,
            video_analysis=None
        )

        results = {
            "interview_id": interview_id,
            "user_id": user_id,
            "interview_type": interview["interview_type"],
            "mode": interview["mode"],
            "overall_score": feedback["overall_score"],
            "scores": feedback["scores"],
            "strengths": feedback["strengths"],
            "weaknesses": feedback["weaknesses"],
            "detailed_feedback": feedback["detailed_feedback"],
            "created_at": interview["started_at"]
        }

        firebase_service.update_interview(
            interview_id,
            {
                "status": "completed",
                "completed_at": datetime.utcnow(),
                "results": results
            }
        )

        del active_interviews[interview_id]

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- GET RESULTS ----------------
@router.get("/{interview_id}/results")
async def get_interview_results(
    interview_id: str,
    user_id: str = Depends(verify_user)
):
    interview = firebase_service.get_interview(interview_id)

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.get("user_id") != user_id and user_id != "user_123":
        raise HTTPException(status_code=403, detail="Unauthorized")

    results = interview.get("results")

    if not results:
        raise HTTPException(
            status_code=404,
            detail="Results not generated yet"
        )

    return results


# ---------------- HISTORY ----------------
@router.get("/history/{user_id}")
async def get_interview_history(user_id: str):
    interviews = firebase_service.get_user_interviews(user_id)
    return {"interviews": interviews}
