from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rag import chat as rag_chat
from app.api import urdu_translate, auth, users, notes, progress, activity

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Book Backend",
    description="Backend for the Physical AI & Humanoid Robotics Book online platform.",
    version="0.1.0"
)

# Determine allowed origins for CORS
allowed_origins = []
if settings.FRONTEND_URL: # Check if the string is not empty
    allowed_origins = [settings.FRONTEND_URL]
    logger.info(f"CORS middleware configured for origin: {settings.FRONTEND_URL}")
else:
    logger.warning("FRONTEND_URL is not set or is empty. CORS will be configured with no specific allowed origins, potentially restricting frontend access.")


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the RAG chat router
app.include_router(rag_chat.router, prefix="/api/rag", tags=["RAG"])
app.include_router(urdu_translate.router, prefix="/api", tags=["translation"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(progress.router, prefix="/api/progress", tags=["progress"])
app.include_router(activity.router, prefix="/api/activity", tags=["activity"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the AI Book Backend"}
