import logging
import re
from qdrant_client import QdrantClient
import httpx

from app.core.config import settings
from app.core.openai import openai_client, OPENAI_CLIENT_ENABLED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetrievalError(Exception):
    """Custom exception for errors during Qdrant retrieval."""
    pass

# --- Configuration ---
EMBEDDING_MODEL = 'text-embedding-3-large'
EXPECTED_DIMENSION = 3072
SIMILARITY_THRESHOLD = 0.5

# --- Global Variables ---
qdrant_client = None
# embedding_model = None # No longer initialized here; OpenAI client handles embeddings
RAG_ENABLED = False

# --- Initialization Logic ---
logger.info("Attempting to initialize Qdrant client and prepare for OpenAI embeddings...")
if settings.QDRANT_URL and settings.QDRANT_COLLECTION_NAME and settings.QDRANT_API_KEY:
    try:
        logger.info("OpenAI client will handle embeddings.")

        logger.info(f"Connecting to Qdrant at {settings.QDRANT_URL}...")
        qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY, timeout=20)
        
        logger.info("Performing Qdrant health check...")
        qdrant_client.get_collections() 
        logger.info("✅ Successfully connected to Qdrant and passed health check.")

        try:
            logger.info(f"Checking for collection '{settings.QDRANT_COLLECTION_NAME}'...")
            collection_info = qdrant_client.get_collection(collection_name=settings.QDRANT_COLLECTION_NAME)
            
            if collection_info.status == 'green' and collection_info.points_count > 0:
                logger.info(f"Collection '{settings.QDRANT_COLLECTION_NAME}' loaded with {collection_info.points_count} points. RAG is ENABLED.")    
                RAG_ENABLED = True
            elif collection_info.status == 'green' and collection_info.points_count == 0:
                logger.warning(f"Collection '{settings.QDRANT_COLLECTION_NAME}' is empty. RAG is DISABLED.")
            else:
                logger.warning(f"Collection '{settings.QDRANT_COLLECTION_NAME}' has status '{collection_info.status}'. RAG is DISABLED.")

        except Exception as e:
            logger.error(f"⚠️ Error checking Qdrant collection '{settings.QDRANT_COLLECTION_NAME}': {e}. RAG is DISABLED.", exc_info=True)       
            RAG_ENABLED = False

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            logger.error(f"❌ Qdrant connection failed with 403 Forbidden. Check QDRANT_API_KEY permissions. RAG will be DISABLED.", exc_info=True)
        else:
            logger.error(f"❌ Qdrant connection failed with HTTP status {e.response.status_code}: {e}. RAG will be DISABLED.", exc_info=True)
        qdrant_client = None
        RAG_ENABLED = False
    except Exception as e:
        logger.error(f"❌ Qdrant initialization failed: {e}. RAG is DISABLED.", exc_info=True)
        qdrant_client = None
        RAG_ENABLED = False
else:
    logger.warning("⚠️ QDRANT_URL, QDRANT_API_KEY, or QDRANT_COLLECTION_NAME not fully set. RAG is DISABLED.")

if RAG_ENABLED:
    logger.info("✅ RAG tool is initialized and ready.")
else:
    logger.info("ℹ️ RAG tool is disabled.")


def _normalize_query(query: str) -> str:
    """
    Cleans and normalizes a query by removing common prefixes and special characters.
    """
    normalized_query = re.sub(r'^(chapter|section|sec\.|part|p\.)?\s*[\d\.]+\s*', '', query.strip(), flags=re.IGNORECASE)
    normalized_query = normalized_query.rstrip('?').strip()
    return normalized_query


async def retrieve_from_book(query: str, top_k: int = 5) -> str:
    """
    Retrieves context from Qdrant by explicitly generating embeddings with FastEmbed
    and using the qdrant_client.query_points() method.
    """
    if not RAG_ENABLED or not qdrant_client: # embedding_model is no longer needed in this check
        logger.warning("RAG is disabled or not configured. Skipping retrieval.")
        return ""

    try:
        original_query = query
        normalized_query = _normalize_query(original_query)
        logger.info(f"Original query: '{original_query}', Normalized query: '{normalized_query}'")

        # Generate embedding explicitly with OpenAI
        logger.info("Generating embedding with OpenAI...")
        if not OPENAI_CLIENT_ENABLED:
            raise RetrievalError("OpenAI client is not enabled for embedding generation.")
        
        response = await openai_client.embeddings.create(input=[normalized_query], model=EMBEDDING_MODEL)
        query_embedding = response.data[0].embedding
        logger.info("✅ Embedding generated successfully.")
        
        logger.info(f"Searching collection '{settings.QDRANT_COLLECTION_NAME}' with top_k={top_k}")

        retrieved_points = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_embedding, # Pass the vector as a list of floats directly from OpenAI response
            limit=top_k,
            with_payload=True
        )
        logger.info(f"Qdrant query_points returned {len(retrieved_points.points)} points.")

        if not retrieved_points.points:
            logger.warning("No matching documents found in Qdrant. Final decision: No context.")
            return ""

        # Log scores for debugging
        scores = [hit.score for hit in retrieved_points.points]
        logger.info(f"Retrieved point scores: {scores}")

        # Basic thresholding to relax retrieval
        if max(scores) < SIMILARITY_THRESHOLD:
            logger.warning(f"Max similarity score {max(scores)} is below threshold {SIMILARITY_THRESHOLD}. Considering this a weak match, but proceeding.")
            # Even if it's a weak match, we proceed as per the "Relaxed Threshold" requirement
        
        context = ""
        retrieved_ids = [hit.id for hit in retrieved_points.points]
        logger.info(f"Retrieved point IDs: {retrieved_ids}")

        for hit in retrieved_points.points: 
            if hit.payload and 'content' in hit.payload:
                context += hit.payload['content'] + "\n\n"
                logger.debug(f"Retrieved chunk ID: {hit.id}, score: {hit.score}, text: {hit.payload['content'][:100]}...")
        
        final_decision = f"Retrieved {len(retrieved_points.points)} documents from Qdrant successfully."
        logger.info(f"✅ Final retrieval decision: {final_decision}")
        return context.strip()

    except Exception as e:
        logger.error(f"ERROR: Qdrant retrieval failed during query for query '{query}': {e}", exc_info=True)
        raise RetrievalError(f"Qdrant retrieval failed: {e}") from e