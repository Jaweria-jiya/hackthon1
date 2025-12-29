import logging
from openai import AsyncOpenAI, Timeout
from app.core.config import settings

logger = logging.getLogger(__name__)

# Define a default timeout of 30 seconds for all requests.
DEFAULT_TIMEOUT = Timeout(30.0)

openai_client = None
OPENAI_CLIENT_ENABLED = False

try:
    if settings.OPENAI_API_KEY:
        openai_client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=DEFAULT_TIMEOUT,
        )
        # Optional: Test a simple call to verify the key. Can be commented out for faster startup.
        # await openai_client.models.list()
        OPENAI_CLIENT_ENABLED = True
        logger.info("✅ OpenAI client initialized successfully.")
    else:
        logger.warning("⚠️ OPENAI_API_KEY is not set. OpenAI client will not be initialized.")
except Exception as e:
    logger.error(f"❌ OpenAI client initialization failed: {e}. AI functionalities dependent on OpenAI might be affected.", exc_info=True)