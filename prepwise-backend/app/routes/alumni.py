from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
import uuid
from datetime import datetime
import firebase_admin.auth

from app.services.firebase_service import FirebaseService

router = APIRouter(prefix="/alumni", tags=["alumni"])

firebase_service = FirebaseService()

# ---------------- AUTH (DEV SAFE) ----------------
def verify_user(authorization: Optional[str] = Header(None)):
    # DEV MODE (no auth break)
    if not authorization or not authorization.startswith("Bearer "):
        return "user_123"

    try:
        token = authorization.replace("Bearer ", "")
        decoded = firebase_admin.auth.verify_id_token(token)
        return decoded.get("uid", "user_123")
    except Exception:
        return "user_123"


# =================================================
# 🔹 STATIC ROUTES (ALWAYS ON TOP)
# =================================================

@router.get("/")
async def get_alumni_directory(
    page: int = 1,
    limit: int = 20,
    verified_only: bool = False
):
    try:
        return firebase_service.get_alumni_list(page, limit, verified_only)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pending/list")
async def get_pending_alumni():
    try:
        pending = firebase_service.get_pending_alumni()
        return {"pending_alumni": pending}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/profile")
async def submit_alumni_profile(
    profile_data: dict,
    user_id: str = Depends(verify_user)
):
    try:
        existing = firebase_service.get_alumni_profile(user_id)

        alumni_data = {
            "user_id": user_id,
            "name": profile_data.get("name", ""),
            "company": profile_data.get("company", ""),
            "role": profile_data.get("role", ""),
            "department": profile_data.get("department", ""),
            "batch": profile_data.get("batch", ""),
            "linkedin_url": profile_data.get("linkedinUrl", ""),
            "availability": profile_data.get("availability", True),
        }

        if not existing:
            alumni_data["verificationStatus"] = "pending"
            alumni_data["verified"] = False
            firebase_service.create_alumni_profile(user_id, alumni_data)
            return {
                "message": "Profile submitted for verification",
                "status": "pending"
            }
        else:
            firebase_service.update_alumni_profile(user_id, alumni_data)
            return {
                "message": "Profile updated successfully",
                "status": existing.get("verificationStatus", "pending")
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/requests")
async def get_alumni_requests(
    user_id: str = Depends(verify_user)
):
    try:
        requests = firebase_service.get_alumni_mentorship_requests(user_id)
        return {"requests": requests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/requests/accept")
async def accept_request(
    data: dict,
    user_id: str = Depends(verify_user)
):
    request_id = data.get("request_id")
    if not request_id:
        raise HTTPException(status_code=400, detail="request_id required")

    firebase_service.update_mentorship_request_status(request_id, "accepted")
    return {"status": "accepted"}


@router.post("/requests/reject")
async def reject_request(
    data: dict,
    user_id: str = Depends(verify_user)
):
    request_id = data.get("request_id")
    if not request_id:
        raise HTTPException(status_code=400, detail="request_id required")

    firebase_service.update_mentorship_request_status(request_id, "rejected")
    return {"status": "rejected"}


@router.post("/{alumni_id}/mentorship")
async def request_mentorship(
    alumni_id: str,
    data: dict,
    user_id: str = Depends(verify_user)
):
    try:
        request_id = str(uuid.uuid4())
        firebase_service.create_mentorship_request(request_id, {
            "user_id": user_id,
            "alumni_id": alumni_id,
            "message": data.get("message", ""),
            "status": "pending",
            "created_at": datetime.utcnow()
        })
        return {"request_id": request_id, "status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =================================================
# 🔻 DYNAMIC ROUTE (ALWAYS LAST)
# =================================================

@router.get("/{alumni_id}")
async def get_alumni_profile(alumni_id: str):
    try:
        profile = firebase_service.get_alumni_profile(alumni_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Alumni not found")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
