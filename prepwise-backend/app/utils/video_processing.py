try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None
from typing import List, Optional
import io

def extract_frames(video_bytes: bytes, frame_rate: int = 1) -> List[np.ndarray]:
    """
    Extract frames from video for analysis
    frame_rate: Extract 1 frame every N seconds
    """
    frames = []
    try:
        # Convert bytes to numpy array for OpenCV
        nparr = np.frombuffer(video_bytes, np.uint8)
        
        # Write to temporary file or use memory buffer
        # For simplicity, we'll use a temporary approach
        # In production, use proper video processing with ffmpeg
        
        # Placeholder - in production use cv2.VideoCapture or ffmpeg
        return frames
    except Exception as e:
        print(f"Error extracting video frames: {e}")
        return []

def extract_frame_from_bytes(video_bytes: bytes, frame_number: int = 0) -> Optional[np.ndarray]:
    """
    Extract a specific frame from video bytes
    """
    try:
        frames = extract_frames(video_bytes, frame_rate=1)
        if frames and frame_number < len(frames):
            return frames[frame_number]
        return None
    except Exception as e:
        print(f"Error extracting frame: {e}")
        return None
