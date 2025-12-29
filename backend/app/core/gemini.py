import logging
from openai import AsyncOpenAI, Timeout
from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize the client to be used for Gemini, pointing to the specified
# OpenAI-compatible base URL for Gemini.
gemini_compatible_client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL,
    timeout=Timeout(60.0),
    max_retries=5,
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "ai-book-chatbot",
    }
)

logger.info("✅ Gemini LLM authenticated successfully.")
logger.info(
    f"   -> Using model '{settings.GEMINI_MODEL}' via base URL: {settings.GEMINI_BASE_URL}"
)
