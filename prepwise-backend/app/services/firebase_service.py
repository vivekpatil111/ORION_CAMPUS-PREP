import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional, Dict, List
from datetime import datetime
import os
from app.config import settings

# #region agent log
import json
log_path = r"c:\Users\shlok\OneDrive\Desktop\prepwise_interview\.cursor\debug.log"
def log_debug(location, message, data=None, hypothesis_id="D"):
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

# Initialize Firebase Admin
# #region agent log
log_debug("firebase_service.py:init_start", "Firebase initialization starting", {}, "D")
# #endregion

try:
    if not firebase_admin._apps:
        # #region agent log
        log_debug("firebase_service.py:init_check", "Firebase not initialized, starting init", {
            "has_credentials_path": bool(settings.FIREBASE_CREDENTIALS_PATH),
            "project_id": settings.FIREBASE_PROJECT_ID
        }, "D")
        # #endregion
        
        if settings.FIREBASE_CREDENTIALS_PATH:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            # #region agent log
            log_debug("firebase_service.py:init_cred_file", "Using credentials file", {
                "path": settings.FIREBASE_CREDENTIALS_PATH
            }, "D")
            # #endregion
        else:
            # Use default credentials (for Cloud Run)
            cred = credentials.ApplicationDefault()
            # #region agent log
            log_debug("firebase_service.py:init_cred_default", "Using default credentials", {}, "D")
            # #endregion
        
        firebase_admin.initialize_app(cred, {
            'projectId': settings.FIREBASE_PROJECT_ID
        })
        # #region agent log
        log_debug("firebase_service.py:init_success", "Firebase initialized successfully", {}, "D")
        # #endregion
    else:
        # #region agent log
        log_debug("firebase_service.py:init_skip", "Firebase already initialized", {}, "D")
        # #endregion
except Exception as e:
    # #region agent log
    log_debug("firebase_service.py:init_error", "Firebase initialization failed", {
        "error": str(e),
        "type": type(e).__name__
    }, "D")
    # #endregion
    # Don't raise - allow app to continue without Firebase for now
    pass

try:
    db = firestore.client()
    # #region agent log
    log_debug("firebase_service.py:db_client", "Firestore client created", {}, "D")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("firebase_service.py:db_client_error", "Firestore client creation failed", {
        "error": str(e)
    }, "D")
    # #endregion
    db = None

class FirebaseService:
    @staticmethod
    def create_user(user_id: str, user_data: Dict) -> None:
        """Create a new user in Firestore"""
        user_ref = db.collection('users').document(user_id)
        user_data['created_at'] = datetime.utcnow()
        user_ref.set(user_data)

    @staticmethod
    def get_user(user_id: str) -> Optional[Dict]:
        """Get user data from Firestore"""
        user_ref = db.collection('users').document(user_id)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    @staticmethod
    def create_interview(interview_id: str, interview_data: Dict) -> None:
        """Save interview data to Firestore"""
        interview_ref = db.collection('interviews').document(interview_id)
        interview_data['created_at'] = datetime.utcnow()
        interview_ref.set(interview_data)

    @staticmethod
    def update_interview(interview_id: str, updates: Dict) -> None:
        """Update interview data"""
        interview_ref = db.collection('interviews').document(interview_id)
        interview_ref.update(updates)

    @staticmethod
    def get_interview(interview_id: str) -> Optional[Dict]:
        """Get interview data"""
        interview_ref = db.collection('interviews').document(interview_id)
        doc = interview_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    @staticmethod
    def get_user_interviews(user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's interview history"""
        interviews_ref = db.collection('interviews')
        query = interviews_ref.where('user_id', '==', user_id).order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def create_alumni_profile(alumni_id: str, alumni_data: Dict) -> None:
        """Create alumni profile"""
        alumni_ref = db.collection('alumni').document(alumni_id)
        alumni_data['created_at'] = datetime.utcnow()
        alumni_ref.set(alumni_data)

    @staticmethod
    def update_alumni_profile(alumni_id: str, updates: Dict) -> None:
        """Update alumni profile"""
        alumni_ref = db.collection('alumni').document(alumni_id)
        updates['updated_at'] = datetime.utcnow()
        alumni_ref.update(updates)

    @staticmethod
    def get_alumni_profile(alumni_id: str) -> Optional[Dict]:
        """Get alumni profile"""
        alumni_ref = db.collection('alumni').document(alumni_id)
        doc = alumni_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None

    @staticmethod
    def get_alumni_list(page: int = 1, limit: int = 20, verified_only: bool = False) -> Dict:
        """Get paginated alumni list"""
        alumni_ref = db.collection('alumni')
        
        if verified_only:
            query = alumni_ref.where('verified', '==', True).limit(limit)
        else:
            query = alumni_ref.limit(limit)
        
        # Note: Firestore admin SDK doesn't support offset directly
        # For MVP, we'll use limit only
        docs = list(query.stream())
        alumni_list = [doc.to_dict() for doc in docs]
        
        return {
            'alumni': alumni_list,
            'has_more': len(docs) == limit
        }

    @staticmethod
    def verify_alumni(alumni_id: str, verified: bool) -> None:
        """Verify/unverify alumni"""
        alumni_ref = db.collection('alumni').document(alumni_id)
        update_data = {
            'verified': verified,
            'verificationStatus': 'verified' if verified else 'rejected'
        }
        if verified:
            update_data['verified_at'] = datetime.utcnow()
        alumni_ref.update(update_data)

    @staticmethod
    def create_mentorship_request(request_id: str, request_data: Dict) -> None:
        """Create mentorship request"""
        request_ref = db.collection('mentorship_requests').document(request_id)
        request_data['created_at'] = datetime.utcnow()
        request_data['status'] = 'pending'
        request_ref.set(request_data)

    @staticmethod
    def get_mentorship_requests(user_id: str) -> List[Dict]:
        """Get mentorship requests for a user"""
        requests_ref = db.collection('mentorship_requests')
        query = requests_ref.where('user_id', '==', user_id).order_by('created_at', direction=firestore.Query.DESCENDING)
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def get_alumni_mentorship_requests(alumni_id: str) -> List[Dict]:
        """Get mentorship requests for an alumni"""
        requests_ref = db.collection('mentorship_requests')
        query = requests_ref.where('alumni_id', '==', alumni_id).order_by('created_at', direction=firestore.Query.DESCENDING)
        docs = query.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)
        return results

    @staticmethod
    def update_mentorship_request_status(request_id: str, status: str) -> None:
        """Update mentorship request status"""
        request_ref = db.collection('mentorship_requests').document(request_id)
        request_ref.update({
            'status': status,
            'updated_at': datetime.utcnow()
        })

    @staticmethod
    def get_mentorship_request(request_id: str) -> Optional[Dict]:
        """Get mentorship request by ID"""
        request_ref = db.collection('mentorship_requests').document(request_id)
        doc = request_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None

    @staticmethod
    def get_pending_alumni() -> List[Dict]:
        """Get all alumni profiles with pending verification status"""
        alumni_ref = db.collection('alumni')
        # Query for pending or unverified alumni
        query = alumni_ref.where('verificationStatus', '==', 'pending')
        docs = list(query.stream())
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            results.append(data)
        
        return results
