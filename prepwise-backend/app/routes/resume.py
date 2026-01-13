from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import Dict

from app.services.resume_parser import ResumeParser
from app.utils.validators import validate_file_extension

router = APIRouter(prefix="/resume", tags=["resume"])

resume_parser = ResumeParser()

def verify_user(token: str = None):
    """Verify Firebase token - placeholder"""
    return "user_123"

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(verify_user)
):
    """Upload resume file"""
    try:
        # Validate file type
        if not validate_file_extension(file.filename, ['.pdf', '.docx']):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")
        
        # Read file
        file_bytes = await file.read()
        
        # In production, save file to cloud storage (Firebase Storage, S3, etc.)
        # For now, just parse and return
        
        return {
            'message': 'Resume uploaded successfully',
            'filename': file.filename,
            'size': len(file_bytes)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(verify_user)
):
    """Parse resume file and extract information"""
    try:
        # Validate file type
        if not validate_file_extension(file.filename, ['.pdf', '.docx']):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")
        
        # Check file size (max 10MB)
        file_bytes = await file.read()
        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        # Parse resume
        parsed_data = resume_parser.parse_resume(file_bytes, file.filename)
        
        return {
            'success': True,
            'data': parsed_data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
