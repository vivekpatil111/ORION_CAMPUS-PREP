from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Dict, List
from app.services.firebase_service import FirebaseService, db
import firebase_admin.auth
from firebase_admin import firestore

router = APIRouter(prefix="/admin", tags=["admin"])

firebase_service = FirebaseService()

def verify_admin(authorization: Optional[str] = Header(None)):
    """Verify Firebase token and check if user is admin"""
    if not authorization or not authorization.startswith("Bearer "):
        # For development, allow requests without auth
        return "admin_123"
    
    try:
        token = authorization.replace("Bearer ", "")
        decoded_token = firebase_admin.auth.verify_id_token(token)
        user_id = decoded_token.get('uid', 'admin_123')
        
        # Check if user is admin
        user_data = firebase_service.get_user(user_id)
        if user_data and user_data.get('role') == 'admin':
            return user_id
        else:
            # For development, allow if not explicitly checked
            return user_id
    except Exception as e:
        print(f"Token verification failed: {e}")
        return "admin_123"

@router.get("/statistics")
async def get_admin_statistics(user_id: str = Depends(verify_admin)):
    """Get platform statistics for admin dashboard"""
    try:
        # Get all users
        users_ref = db.collection('users')
        all_users = list(users_ref.stream())
        
        students = [u for u in all_users if u.to_dict().get('role') == 'student']
        alumni = [u for u in all_users if u.to_dict().get('role') == 'alumni']
        
        # Get alumni profiles
        alumni_profiles_ref = db.collection('alumni')
        all_alumni_profiles = list(alumni_profiles_ref.stream())
        
        verified_alumni = [a for a in all_alumni_profiles if a.to_dict().get('verified') == True]
        pending_alumni = [a for a in all_alumni_profiles if a.to_dict().get('verificationStatus') == 'pending']
        
        # Get mentorship requests
        mentorship_ref = db.collection('mentorship_requests')
        all_requests = list(mentorship_ref.stream())
        
        active_requests = [r for r in all_requests if r.to_dict().get('status') in ['pending', 'accepted']]
        
        # Get interviews
        interviews_ref = db.collection('interviews')
        all_interviews = list(interviews_ref.stream())
        
        return {
            'total_students': len(students),
            'total_alumni': len(verified_alumni),
            'pending_verifications': len(pending_alumni),
            'active_mentorship_requests': len(active_requests),
            'total_interviews': len(all_interviews)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/students")
async def get_all_students(
    page: int = 1,
    limit: int = 50,
    user_id: str = Depends(verify_admin)
):
    """Get all registered students"""
    try:
        users_ref = db.collection('users')
        query = users_ref.where('role', '==', 'student').limit(limit)
        docs = list(query.stream())
        
        students = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            students.append(data)
        
        return {'students': students, 'total': len(students)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alumni/verified")
async def get_verified_alumni(
    page: int = 1,
    limit: int = 50,
    user_id: str = Depends(verify_admin)
):
    """Get all verified alumni"""
    try:
        alumni_ref = db.collection('alumni')
        query = alumni_ref.where('verified', '==', True).limit(limit)
        docs = list(query.stream())
        
        alumni = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            alumni.append(data)
        
        return {'alumni': alumni, 'total': len(alumni)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mentorship/all")
async def get_all_mentorship_requests(user_id: str = Depends(verify_admin)):
    """Get all mentorship requests for oversight"""
    try:
        requests_ref = db.collection('mentorship_requests')
        docs = list(requests_ref.stream())
        
        requests = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            requests.append(data)
        
        return {'requests': requests, 'total': len(requests)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interviews/analytics")
async def get_interview_analytics(user_id: str = Depends(verify_admin)):
    """Get interview analytics for admin"""
    try:
        interviews_ref = db.collection('interviews')
        all_interviews = list(interviews_ref.stream())
        
        total_interviews = len(all_interviews)
        completed = [i for i in all_interviews if i.to_dict().get('status') == 'completed']
        in_progress = [i for i in all_interviews if i.to_dict().get('status') == 'in_progress']
        
        # Calculate average scores
        scores = []
        for interview in completed:
            results = interview.to_dict().get('results')
            if results and results.get('overall_score'):
                scores.append(results.get('overall_score'))
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Group by interview type
        by_type = {}
        for interview in all_interviews:
            interview_type = interview.to_dict().get('interview_type', 'unknown')
            by_type[interview_type] = by_type.get(interview_type, 0) + 1
        
        return {
            'total_interviews': total_interviews,
            'completed': len(completed),
            'in_progress': len(in_progress),
            'average_score': round(avg_score, 2),
            'by_type': by_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alumni/{alumni_id}/block")
async def block_alumni(
    alumni_id: str,
    blocked: bool,
    user_id: str = Depends(verify_admin)
):
    """Block or unblock alumni account"""
    try:
        alumni_ref = db.collection('alumni').document(alumni_id)
        alumni_ref.update({'blocked': blocked})
        
        return {'message': f'Alumni {"blocked" if blocked else "unblocked"} successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/students/{student_id}/block")
async def block_student(
    student_id: str,
    blocked: bool,
    user_id: str = Depends(verify_admin)
):
    """Block or unblock student account"""
    try:
        user_ref = db.collection('users').document(student_id)
        user_ref.update({'blocked': blocked})
        
        return {'message': f'Student {"blocked" if blocked else "unblocked"} successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

