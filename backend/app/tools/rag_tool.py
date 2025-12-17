import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from openai import AuthenticationError, APIError
from pydantic import Field, BaseModel

from app.core.config import gemini_client, settings # Import settings

# Remove redundant load_dotenv() as it's handled in app.core.config
# QDRANT_HOST = os.getenv("QDRANT_HOST")
# QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_book") # Still allow override for collection name

# Remove redundant check, now handled in app.core.config
# if not QDRANT_HOST:
#     raise ValueError("QDRANT_HOST environment variable not set.")

qdrant_client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    api_key=settings.QDRANT_API_KEY,
) # Use settings object

def retrieve_from_book(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieves relevant document chunks from the 'Physical AI & Humanoid Robotics Book' based on a user query.
    """
    try:
        embedding_response = gemini_client.embeddings.create(
            model="embedding-001",
            input=query,
        )
        query_vector = embedding_response.data[0].embedding
    except AuthenticationError as e:
        raise ValueError(f"Gemini API Authentication Error for embeddings: {e}")
    except APIError as e:
        raise RuntimeError(f"Gemini API Error for embeddings: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to generate embedding for query using Gemini API: {e}")

    try:
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            score_threshold=0.7
        )
    except UnexpectedResponse as e:
        raise RuntimeError(f"Qdrant client error during search: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve from Qdrant: {e}")

    results = []
    for hit in search_result:
        payload = hit.payload
        results.append(
            {
                "content": payload.get("content", ""),
                "source": payload.get("source", "unknown"),
                "chunk_id": payload.get("chunk_id", "unknown"),
                "score": hit.score
            }
        )
    return results

rag_retrieval_tool_def = {
    "type": "function",
    "function": {
        "name": "retrieve_from_book",
        "description": "Retrieves relevant document chunks from the 'Physical AI & Humanoid Robotics Book' based on a user query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's query for retrieving relevant information from the book."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of relevant chunks to retrieve."
                }
            },
            "required": ["query"]
        }
    }
}

available_tools = {
    "retrieve_from_book": retrieve_from_book,
}