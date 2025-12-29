import logging
import os
import sys

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_environment_check():
    """
    Diagnoses the qdrant-client installation and environment.
    """
    logger.info("--- Starting Qdrant Environment Verification Script ---")

    try:
        # --- 0. Environment Safety Check ---
        logger.info("--- Python Environment Details ---")
        logger.info(f"Python Executable: {sys.executable}")
        
        import subprocess
        pip_version_result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
        if pip_version_result.returncode == 0:
            logger.info(f"Pip Version Details: {pip_version_result.stdout.strip()}")
        else:
            logger.error(f"Could not determine pip version: {pip_version_result.stderr}")
        logger.info("---------------------------------")


        # --- 1. Check Qdrant Client Installation ---
        logger.info("Checking 'qdrant-client' installation...")
        import qdrant_client
        from qdrant_client.http import models
        
        # This part of the script uses SentenceTransformer, but the main app uses FastEmbed.
        # This is for a standalone check and might differ from the app's internal logic.
        from sentence_transformers import SentenceTransformer

        # Get version using a robust method
        try:
            from importlib.metadata import version
            client_version = version('qdrant-client')
        except ImportError:
            # Fallback for older python
            import pkg_resources
            client_version = pkg_resources.get_distribution('qdrant-client').version

        logger.info(f"✅ Found qdrant-client version: {client_version}")
        logger.info(f"   Library location: {qdrant_client.__file__}")

        # --- 2. Load Environment Variables ---
        logger.info("Loading environment variables from 'backend/.env'...")
        project_root = os.path.dirname(os.path.abspath(__file__))
        backend_env_path = os.path.join(project_root, "backend", ".env")
        if not os.path.exists(backend_env_path):
            logger.error(f"FATAL: Could not find '.env' file at {backend_env_path}")
            sys.exit(1)

        from dotenv import load_dotenv
        load_dotenv(dotenv_path=backend_env_path)

        QDRANT_URL = os.getenv("QDRANT_URL")
        QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
        QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

        if not all([QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME]):
            logger.error("FATAL: One or more required Qdrant environment variables are not set in the .env file.")
            sys.exit(1)
        
        logger.info("✅ Environment variables loaded.")
        
        # --- 3. Perform a Live Qdrant Search ---
        logger.info(f"Connecting to Qdrant and performing a test search on collection '{QDRANT_COLLECTION_NAME}'...")
        client = qdrant_client.QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=20)
        
        # This test uses SentenceTransformer. The main app is being refactored to use FastEmbed.
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        query_vector = embedding_model.encode("test query").tolist()

        search_result = client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=1
        )
        
        logger.info("✅ Live search API call executed successfully.")
        logger.info(f"   Search returned {len(search_result)} points.")
        if search_result:
            logger.info(f"   Type of first result: {type(search_result[0])}")

        logger.info("\n--- DIAGNOSIS ---")
        logger.info("Script completed. Review the Python environment details above.")
        logger.info("Ensure the Python executable and pip location point to your project's virtual environment.")
        logger.info("--------------------")

    except ImportError as e:
        logger.error(f"FATAL IMPORT ERROR: {e}", exc_info=True)
        logger.error("\n--- DIAGNOSIS ---")
        logger.error(f"The Python environment at '{sys.executable}' is missing a required library.")
        logger.error("Solution: Activate this virtual environment and run 'pip install -r backend/requirements.txt'.")
        logger.error("--------------------")
        sys.exit(1)

    except Exception as e:
        logger.error(f"FATAL RUNTIME ERROR: An unexpected error occurred: {e}", exc_info=True)
        logger.error("\n--- DIAGNOSIS ---")
        logger.error("The script failed during execution. The traceback above contains the specific error.")
        logger.error("This could be due to incorrect environment variables (API key, URL), network issues, or another problem.")
        logger.error("Please review the error message to diagnose the problem with your setup.")
        logger.error("--------------------")
        sys.exit(1)

if __name__ == "__main__":
    run_environment_check()
