from typing import Optional
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Validate file extension"""
    return any(filename.lower().endswith(ext.lower()) for ext in allowed_extensions)

def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize user input"""
    # Remove potentially dangerous characters
    text = text.strip()
    if max_length:
        text = text[:max_length]
    return text
