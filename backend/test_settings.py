
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"App Name: {settings.APP_NAME}")
logger.info(f"Database URL: {settings.DATABASE_URL}")
logger.info(f"OpenAI API Key (first 5 chars): {settings.OPENAI_API_KEY[:5]}...")
logger.info(f"Qdrant URL: {settings.QDRANT_URL}")
logger.info(f"Qdrant API Key (first 5 chars): {settings.QDRANT_API_KEY[:5]}...")
logger.info(f"Qdrant Collection Name: {settings.QDRANT_COLLECTION_NAME}")
