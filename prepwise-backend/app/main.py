from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# #region agent log
import json
from datetime import datetime
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

# #region agent log
log_debug("main.py:import_start", "Starting imports", {}, "B")
# #endregion

try:
    from app.routes import interview, alumni, resume, auth, admin, gd
    # #region agent log
    log_debug("main.py:import_success", "All routes imported successfully", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:import_error", "Import failed", {"error": str(e), "type": type(e).__name__}, "B")
    # #endregion
    raise

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# #region agent log
log_debug("main.py:app_created", "FastAPI app instance created", {}, "B")
# #endregion

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
# #region agent log
log_debug("main.py:router_registration_start", "Starting router registration", {}, "B")
# #endregion

try:
    app.include_router(auth.router, prefix="/api")
    # #region agent log
    log_debug("main.py:router_auth", "Auth router registered", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:router_auth_error", "Auth router failed", {"error": str(e)}, "B")
    # #endregion
    raise

try:
    app.include_router(interview.router, prefix="/api")
    # #region agent log
    log_debug("main.py:router_interview", "Interview router registered", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:router_interview_error", "Interview router failed", {"error": str(e)}, "B")
    # #endregion
    raise

try:
    app.include_router(alumni.router, prefix="/api")
    # #region agent log
    log_debug("main.py:router_alumni", "Alumni router registered", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:router_alumni_error", "Alumni router failed", {"error": str(e)}, "B")
    # #endregion
    raise

try:
    app.include_router(resume.router, prefix="/api")
    # #region agent log
    log_debug("main.py:router_resume", "Resume router registered", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:router_resume_error", "Resume router failed", {"error": str(e)}, "B")
    # #endregion
    raise

try:
    app.include_router(admin.router, prefix="/api")
    # #region agent log
    log_debug("main.py:router_admin", "Admin router registered", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:router_admin_error", "Admin router failed", {"error": str(e)}, "B")
    # #endregion
    raise

try:
    app.include_router(gd.router, prefix="/api")
    # #region agent log
    log_debug("main.py:router_gd", "GD router registered", {}, "B")
    # #endregion
except Exception as e:
    # #region agent log
    log_debug("main.py:router_gd_error", "GD router failed", {"error": str(e)}, "B")
    # #endregion
    raise

# #region agent log
log_debug("main.py:router_registration_complete", "All routers registered successfully", {}, "B")
# #endregion

@app.get("/")
async def root():
    return {
        "message": "PrepWise API",
        "version": settings.VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
