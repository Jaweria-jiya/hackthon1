import logging
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    APP_NAME: str = "AI Book Backend"
    DATABASE_URL: str = "sqlite:///./test.db"

    # OpenAI API Key
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")

    # Gemini API Key
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")

    # Qdrant Configuration
    QDRANT_URL: str = Field(..., env="QDRANT_URL")
    QDRANT_API_KEY: str = Field(..., env="QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = Field(..., env="QDRANT_COLLECTION_NAME")

    # Frontend Configuration
    FRONTEND_URL: str = Field("http://localhost:3000", env="FRONTEND_URL")

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

# Initialize settings
try:
    settings = Settings()
    logger.info("✅ Environment variables loaded successfully using Pydantic.")
except Exception as e:
    logger.error(f"❌ Failed to load environment variables: {e}")
    # It's critical to exit if basic settings cannot be loaded
    # For a FastAPI app, you might want to raise an exception that stops the app startup
    raise RuntimeError("Failed to load environment variables. Please check your .env file.") from e