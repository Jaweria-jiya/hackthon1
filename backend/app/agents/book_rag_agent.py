import asyncio
import logging
from openai import AsyncOpenAI  # Keep this import for type hinting/consistency if needed, but not for instantiation
# Import the pre-initialized OpenAI client and its status from app.core.openai
from app.core.openai import openai_client, OPENAI_CLIENT_ENABLED

from app.tools.rag_tool import retrieve_from_book, RetrievalError # Import RetrievalError
from app.core.config import settings
# from app.core.openai import openai_client # Removed, as it's now imported above

logger = logging.getLogger(__name__) # Initialize logger

SYSTEM_PROMPT = """You are a helpful assistant that answers questions by synthesizing information from provided book excerpts. Your role is content synthesis and explanation. You must not use any external knowledge. Your job is to construct a clear, book-faithful answer from all relevant context provided."""

async def generate_answer(query: str) -> str:
    """
    Generates a response by first classifying the user's intent and then
    either using a RAG pipeline for book-related questions or a general LLM
    for conversational queries.
    """
    if not OPENAI_CLIENT_ENABLED:
        logger.warning("OpenAI client is not enabled. Falling back to a predefined response.")
        return "Sorry, the AI services are currently unavailable. Please try again later."

    try:
        # Step 1: Classify the user's intent
        classification_prompt = f"""
        Classify the user's query into one of the following categories: GENERAL_CONVERSATION or BOOK_RELATED_QUESTION.

        - GENERAL_CONVERSATION: For greetings, conversational questions about you (the AI), or topics unrelated to robotics, AI, or the book.
        - BOOK_RELATED_QUESTION: For specific questions about robotics, AI, ROS, or any technical topic that might be in a book about physical AI and robotics.

        User Query: "{query}"

        Category:
        """
        
        logger.info(f"Classifying intent for query: '{query}'")
        classification_response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an intent classification assistant."},
                {"role": "user", "content": classification_prompt},
            ],
            temperature=0.0,
            max_tokens=20,
        )
        intent = classification_response.choices[0].message.content.strip()
        logger.info(f"Classified intent as: {intent}")

        # Step 2: Generate response based on intent
        if "GENERAL_CONVERSATION" in intent:
            logger.info("Handling as a general conversation.")
            general_prompt = "You are a helpful and friendly assistant."
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": general_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content

        else: # Assumes BOOK_RELATED_QUESTION
            logger.info("Handling as a book-related question.")
            context = await retrieve_from_book(query=query)
            
            if not context or not context.strip():
                logger.warning("RAG unavailable or no relevant context found for book-related question.")
                return "Not found in the book."

            logger.info("RAG context retrieved. Using RAG-based prompt.")
            prompt_to_use = f"""
Your task is to answer the user's question based on the provided book context. The context may contain multiple related chunks of text, headings, or summaries. Synthesize the information from all relevant chunks to provide a comprehensive and clear answer.

- Understand the user's question and use all relevant parts of the context to answer it.
- If a definition is implied across paragraphs, reconstruct it.
- Do not add information that is not present in the context.
- Preserve all formatting like headings, bullet points, and diagrams.
- Do not say "Not found in the book" if any relevant information is present.

BOOK CONTEXT:
----------------
{context}
----------------

USER QUESTION:
{query}

ANSWER (synthesized from book context):
"""

            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_to_use},
                ],
                temperature=0.0,
            )
            return response.choices[0].message.content

    except RetrievalError as e:
        logger.error(f"ERROR: Qdrant retrieval failed: {e}", exc_info=True)
        return "Sorry, there was an internal issue retrieving information from the book. Please try again."
    except Exception as e:
        logger.error(f"ERROR in generate_answer: {type(e).__name__} - {e}", exc_info=True)
        return "Sorry, I encountered an unexpected error while processing your request."
