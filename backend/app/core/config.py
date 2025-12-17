from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# 🔒 Force ONLY backend/.env
load_dotenv(dotenv_path=".env", override=True)

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    GEMINI_API_KEY: str

    QDRANT_HOST: str
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "physical_ai_book"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()