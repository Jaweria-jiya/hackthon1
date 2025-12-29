import sys
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# This is a workaround to import the agent from a directory outside the 'backend' app
# A better solution in a production app would be a shared library or a monorepo structure
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "../../../"))
sys.path.append(os.path.join(_PROJECT_ROOT, "agents-openai"))

try:
    from urdu_translation_agent import translate_content_to_urdu
except ImportError:
    # This will fail if the agent file is not found, providing a clear error
    raise RuntimeError("Could not import 'urdu_translation_agent'. Ensure it exists in the 'agents-openai' directory and its dependencies are installed.")

router = APIRouter()

class TranslationRequest(BaseModel):
    content: str

class TranslationResponse(BaseModel):
    translated_content: str

@router.post("/translate/urdu", response_model=TranslationResponse)
async def translate_chapter_to_urdu(request: TranslationRequest):
    """
    Receives chapter content and returns its Urdu translation using the Gemini agent.
    """
    if not request.content:
        raise HTTPException(status_code=400, detail="Content to translate cannot be empty.")

    # The agent function is synchronous, so we call it directly.
    # If it were async, we would await it.
    # Note: Running a potentially long-running, CPU-bound task like this in a main async
    # thread is not ideal. For production, it should be run in a thread pool.
    translated_text = translate_content_to_urdu(request.content)

    if "failed" in translated_text.lower() or "error" in translated_text.lower():
        # Generic error check based on agent's return string
        raise HTTPException(status_code=500, detail=f"Translation failed: {translated_text}")

    return TranslationResponse(translated_content=translated_text)
