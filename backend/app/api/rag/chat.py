from fastapi import APIRouter, Request
import logging
from pydantic import BaseModel
from app.agents.book_rag_agent import generate_answer

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Define Pydantic model for the request body to be used in Swagger UI
class RagQueryRequest(BaseModel):
    query_text: str

@router.post("/query")
async def chat_endpoint(payload: RagQueryRequest, request: Request):
    """
    Receives user queries, processes them via the RAG and LLM agent,
    and returns a JSON response. This endpoint is robust and will always
    return a valid JSON answer.
    """
    # Log incoming request details for debugging
    logger.info(f"Incoming request headers: {request.headers}")
    logger.info(f"Received query from payload: '{payload.query_text}'")
    
    query_text = payload.query_text

    response_text = ""
    # Ensure query_text is not empty or just whitespace
    if not query_text or not query_text.strip():
        logger.error("Query text is empty. Returning a fallback response.")
        response_text = "I'm sorry, I didn't understand your request. Could you please rephrase it?"
    else:
        logger.info(f"Processing query: '{query_text}'")
        try:
            # Call the agent to get the LLM's answer
            response_text = await generate_answer(query_text)
        except Exception as e:
            # Catch-all for any unexpected errors from the agent
            logger.error(f"FATAL: Unhandled error in generate_answer: {e}", exc_info=True)
            response_text = "Sorry, an internal error occurred."

    # Always return a 200 OK with the required JSON structure
    answer = response_text
    logger.info(f"Returning answer to client: {answer}")
    return {"answer": answer}