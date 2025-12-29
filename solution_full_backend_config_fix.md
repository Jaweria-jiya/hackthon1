# Part 1: Modifications to `backend/app/core/config.py`

```python
import logging
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import sys

# Determine the project root to correctly locate backend/.env
# This assumes this file is located at `backend/app/core/config.py`
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "../../.."))

# Path to the backend-specific .env file
backend_env_path = os.path.join(_PROJECT_ROOT, "backend", ".env")

# Ensure the .env file exists before attempting to load
if not os.path.exists(backend_env_path):
    logging.error(f"FATAL: backend/.env file not found at {backend_env_path}. Please create it with necessary variables.")
    sys.exit(1)

load_dotenv(dotenv_path=backend_env_path, override=True)
logging.info(f"✅ Loaded .env file from: {backend_env_path}")


class Settings(BaseSettings):
    # Core Application
    DATABASE_URL: str
    SECRET_KEY: str
    FRONTEND_URL: str = "http://localhost:3000"

    # API Keys & Services
    OPENAI_API_KEY: str # Added this attribute

    # Gemini LLM Provider (Assuming these are still needed)
    GEMINI_API_KEY: Optional[str] = None # Made optional for flexibility
    GEMINI_MODEL: str = "gemini-pro"
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    
    # Qdrant RAG Storage
    QDRANT_URL: str # Made mandatory
    QDRANT_API_KEY: str # Made mandatory
    QDRANT_COLLECTION_NAME: str = "physical_ai_book"

    model_config = SettingsConfigDict(
        env_file=backend_env_path, # Explicitly point to backend/.env
        extra="ignore"
    )

settings = Settings()

# Validate critical settings immediately after loading
if not settings.OPENAI_API_KEY:
    logging.error("FATAL: OPENAI_API_KEY is not set in backend/.env")
    sys.exit(1)
if not settings.QDRANT_URL:
    logging.error("FATAL: QDRANT_URL is not set in backend/.env")
    sys.exit(1)
if not settings.QDRANT_API_KEY:
    logging.error("FATAL: QDRANT_API_KEY is not set in backend/.env")
    sys.exit(1)
if not settings.QDRANT_COLLECTION_NAME:
    logging.error("FATAL: QDRANT_COLLECTION_NAME is not set in backend/.env")
    sys.exit(1)

logging.info("✅ All critical environment variables validated.")
```

**Part 2: Snippet for Qdrant and OpenAI initialization (Suggested to be placed in `backend/app/core/clients.py` for modularity)**

```python
import logging
import sys
from typing import Optional
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse, ResponseHandlingException
import openai # Using the official openai client

from app.core.config import settings # Import the Pydantic settings

logger = logging.getLogger(__name__)

# Global flags and clients
rag_enabled: bool = False
qdrant_client_instance: Optional[QdrantClient] = None # Renamed to avoid conflict with imported QdrantClient class
openai_client_instance: Optional[openai.OpenAI] = None # Store OpenAI client

def initialize_qdrant_rag():
    global rag_enabled, qdrant_client_instance

    logger.info("Attempting to initialize Qdrant RAG client...")

    # Validate QDRANT_URL for localhost as per previous strict rule
    if "localhost" in settings.QDRANT_URL:
        logger.error("FATAL: QDRANT_URL points to localhost. RAG functionality aborted as per rules.")
        sys.exit(1)

    try:
        qdrant_client_instance = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            prefer_grpc=True # Assuming gRPC is preferred for cloud instances
        )
        logger.info(f"Attempting to connect to Qdrant at: {settings.QDRANT_URL}")
        
        # Check connectivity by listing collections (a lightweight operation)
        # This will raise UnexpectedResponse if API key is invalid or connection fails
        qdrant_client_instance.get_collections() 
        logger.info("✅ Qdrant connection successful.")

        # Validate collection existence (do not create/modify)
        try:
            collection_info = qdrant_client_instance.get_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
            logger.info(f"✅ Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' found. Points: {collection_info.points_count}")
            
            # Here, you might add checks for vector config if needed, e.g. 
            # if collection_info.config.params.vectors_config.size != EMBEDDING_DIMENSION:
            #     logger.error("FATAL: Vector dimension mismatch in Qdrant collection.")
            #     sys.exit(1)
            
            rag_enabled = True
            logger.info("✅ RAG functionality ENABLED.")

        except UnexpectedResponse as e:
            if e.status_code == 404:
                logger.error(f"FATAL: Qdrant collection '{settings.QDRANT_COLLECTION_NAME}' not found. Cannot enable RAG. DO NOT CREATE COLLECTION.")
                sys.exit(1) # As per rule: STOP execution if collection does NOT exist
            else:
                raise # Re-raise other unexpected responses

    except UnexpectedResponse as e:
        if e.status_code == 403:
            logger.warning(f"⚠️ Qdrant returned 403 Forbidden. Disabling RAG functionality. Error: {e.content}")
            rag_enabled = False
        else:
            logger.error(f"FATAL: Qdrant connection failed with unexpected response (Status: {e.status_code}). Aborting.")
            sys.exit(1)
    except ResponseHandlingException as e:
        logger.error(f"FATAL: Qdrant connection failed due to network or response handling error: {e}. Aborting.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"FATAL: Qdrant client initialization or connection failed: {e}. Aborting.")
        sys.exit(1)

def get_qdrant_client() -> Optional[QdrantClient]:
    """Returns the initialized Qdrant client instance if RAG is enabled."""
    return qdrant_client_instance if rag_enabled else None

def initialize_openai_client():
    global openai_client_instance
    logger.info("Attempting to initialize OpenAI client...")
    try:
        openai_client_instance = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        # You might add a test call here to confirm the API key is valid if needed
        # e.g., openai_client_instance.models.list()
        logger.info("✅ OpenAI client initialized successfully.")
    except openai.AuthenticationError as e:
        logger.error(f"FATAL: OpenAI client initialization failed due to authentication error: {e}. Aborting.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"FATAL: OpenAI client initialization failed: {e}. Aborting.")
        sys.exit(1)

def get_openai_client() -> Optional[openai.OpenAI]:
    """Returns the initialized OpenAI client instance."""
    return openai_client_instance

# --- Integration points in your FastAPI app's startup event ---
# This part is for conceptual guidance, not part of the snippet to paste.
# Example for main.py or an app_startup_event handler:
# from fastapi import FastAPI
# from app.core.config import settings
# from app.core.clients import initialize_qdrant_rag, initialize_openai_client, rag_enabled, get_qdrant_client, get_openai_client
# 
# app = FastAPI()
# 
# @app.on_event("startup")
# async def startup_event():
#     initialize_openai_client() # Initialize OpenAI client first
#     initialize_qdrant_rag()    # Then Qdrant
# 
#     if rag_enabled:
#         logger.info("Backend started with RAG enabled. Qdrant client available via get_qdrant_client()")
#     else:
#         logger.warning("Backend started with RAG disabled due to Qdrant issues. RAG endpoints should be guarded.")
# 
#     # Other startup tasks...
```

**Part 3: CLI Instructions to test environment variable loading and start the backend safely.**

```bash
# ==============================================================================
# Step 1: MANUALLY CORRECT YOUR `backend/.env` FILE
# ==============================================================================
# The provided .env snippet has a formatting error where OPENAI_API_KEY is empty
# and its value is concatenated into QDRANT_URL. This MUST be corrected manually.

# Your `backend/.env` file should look like this (ensure no extra spaces/lines):
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# OPENAI_API_KEY=
# QDRANT_URL=https://6af31d6d-62e2-4604-bf23-af89de37d205.us-east4-0.gcp.cloud.qdrant.io:6333
# QDRANT_API_KEY=
# QDRANT_COLLECTION_NAME=physical_ai_book
# DATABASE_URL="your_database_url_here" # Ensure all other Pydantic fields in app/core/config.py are also present and valid
# SECRET_KEY="your_secret_key_here"
# FRONTEND_URL="http://localhost:3000"
# GEMINI_API_KEY="your_gemini_api_key_here" # Or leave empty if optional
# GEMINI_MODEL="your_gemini_model_here"
# GEMINI_BASE_URL="your_gemini_base_url_here"
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ==============================================================================
# Step 2: Install Required Python Packages
# ==============================================================================
# Navigate to your project\'s root directory:
cd C:\Users\ALI\Desktop\hackthon\ai-book

# Activate your Python virtual environment (if you have one):
# backend\venv\Scripts\activate

# Install necessary packages (if not already installed):
pip install "pydantic-settings>=2.0" "python-dotenv" "qdrant-client>=1.7.0" "openai" "uvicorn" "fastapi"

# ==============================================================================
# Step 3: Integrate the Provided Python Snippets
# ==============================================================================
# You will need to manually apply the changes from Part 1 to `backend/app/core/config.py`.
# You will also need to create a new file `backend/app/core/clients.py` and paste the code from Part 2 into it.
# Finally, integrate the client initialization calls into your FastAPI app's startup event in `backend/app/main.py`
# (or wherever your FastAPI app's startup logic resides) as shown in the example in Part 2.


# ==============================================================================
# Step 4: Test Environment Loading and Client Initialization
# ==============================================================================
# After applying the code changes and correcting your .env file,
# you can create a temporary Python script (e.g., `backend/test_clients.py`) to verify:

# `backend/test_clients.py` content:
# ```python
# import logging
# import os
# from app.core.config import settings
# from app.core.clients import initialize_qdrant_rag, initialize_openai_client, rag_enabled, qdrant_client_instance, openai_client_instance
# 
# # Configure basic logging for the test script
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# 
# if __name__ == "__main__":
#     print("\n--- Testing Configuration and Client Initialization ---")
#     print(f"Loaded .env from: {os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'backend', '.env')}")
#     
#     # Print parts of keys to confirm loading without exposing full keys
#     print(f"OPENAI_API_KEY (prefix): {settings.OPENAI_API_KEY[:5]}...")
#     print(f"QDRANT_URL: {settings.QDRANT_URL}")
#     print(f"QDRANT_API_KEY (prefix): {settings.QDRANT_API_KEY[:5]}...")
#     print(f"QDRANT_COLLECTION_NAME: {settings.QDRANT_COLLECTION_NAME}")
# 
#     initialize_openai_client()
#     initialize_qdrant_rag()
# 
#     if rag_enabled:
#         print("\n✅ RAG system is expected to be ACTIVE.")
#         # Optional: You can try a dummy Qdrant operation here if you want to further verify
#         # try:
#         #     qdrant_client_instance.get_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
#         #     print(f"   (Verified collection '{settings.QDRANT_COLLECTION_NAME}' access.)")
#         # except Exception as e:
#         #     print(f"   (Warning: Could not perform dummy Qdrant operation: {e})")
#     else:
#         print("\n⚠️ RAG system is expected to be DISABLED.")
# 
#     if openai_client_instance:
#         print("✅ OpenAI client is initialized.")
#     else:
#         print("❌ OpenAI client is NOT initialized (this should not happen if OPENAI_API_KEY is valid and present).")
# 
#     print("--- Test Complete ---")
# ```

# Run the test script:
# python backend/test_clients.py

# ==============================================================================
# Step 5: Start the FastAPI Backend
# ==============================================================================
# If the test script runs successfully and reports RAG as ACTIVE (or gracefully disabled),
# you can then start your FastAPI backend application:
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
```