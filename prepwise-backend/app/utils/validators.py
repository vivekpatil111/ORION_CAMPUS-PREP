from typing import Optional, Sequence
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.fullmatch(pattern, email.strip()) is not None

def validate_file_extension(filename: str, allowed_extensions: Sequence[str]) -> bool:
    """Validate file extension"""
    normalized = filename.strip().lower()
    normalized_extensions = {ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in allowed_extensions}
    return any(normalized.endswith(ext) for ext in normalized_extensions)

def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """Sanitize user input"""
    # Remove potentially dangerous characters
    text = text.strip()
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    if max_length is not None and max_length >= 0:
        text = text[:max_length]
    return text
