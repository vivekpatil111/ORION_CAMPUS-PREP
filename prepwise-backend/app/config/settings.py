from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, List, Union
import json

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None
    
    # App Settings
    APP_NAME: str = "PrepWise API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Audio/Video Processing
    MAX_AUDIO_SIZE_MB: int = 10
    MAX_VIDEO_SIZE_MB: int = 50
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            if not v or v.strip() == '':
                return ["http://localhost:3000", "http://localhost:5173"]
            try:
                return json.loads(v)
            except:
                # If not valid JSON, treat as comma-separated string
                return [origin.strip() for origin in v.split(',') if origin.strip()]
        return ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
