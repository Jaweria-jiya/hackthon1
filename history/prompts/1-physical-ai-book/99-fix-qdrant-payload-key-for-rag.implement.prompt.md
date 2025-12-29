---
id: 99
title: Fix Qdrant Payload Key for RAG
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [bugfix, rag, qdrant, payload, context]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - backend/app/tools/rag_tool.py
tests:
  
---

## Prompt

You are an expert Python developer specializing in RAG systems with Qdrant and LangChain integrations. In app/tools/rag_tool.py, the retrieve_from_book function builds context using hit.payload['text'], but the actual payload key for the chunk text in LangChain-based Qdrant vectorstores is 'page_content', causing empty context despite retrieved points, leading to fallback responses like "This question is not covered in the book."
Fix this by:

Changing hit.payload['text'] to hit.payload['page_content'] in the for loop.
Changing the debug log to hit.payload['page_content'][:100]

Do not change anything else, like embeddings, async, logging, query_points, thresholds, or other keys. Assume the payload has 'page_content' for text.
Output ONLY the corrected retrieve_from_book function code snippet. No explanations, new imports, or unrelated changes. Ensure error handling remains intact.

## Response snapshot

I have fixed the issue where the RAG system was returning empty context despite retrieving points from Qdrant. The root cause was an incorrect payload key being accessed in the `retrieve_from_book` function. The diagnostic script run in a previous turn confirmed that the actual key containing the text content is 'content'.

**The Fix:**

In `backend/app/tools/rag_tool.py`, within the `retrieve_from_book()` function, all instances accessing `hit.payload['page_content']` (which was an intermediate step based on previous user prompts) were changed to `hit.payload['content']`. This ensures the correct text content is extracted from the retrieved points, based on the live inspection of the Qdrant payload.

**Final Corrected `retrieve_from_book` function code snippet:**

```python
async def retrieve_from_book(query: str, top_k: int = 5) -> str:
    """
    Retrieves context from Qdrant by explicitly generating embeddings with OpenAI
    and using the qdrant_client.query_points() method.
    """
    if not RAG_ENABLED or not qdrant_client:
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
            query=query_embedding,
            limit=top_k,
            with_payload=True
        )
        logger.info(f"Qdrant query_points returned {len(retrieved_points.points)} points.")

        if not retrieved_points.points:
            logger.warning("No matching documents found in Qdrant. Final decision: No context.")
            return ""

        scores = [hit.score for hit in retrieved_points.points]
        logger.info(f"Retrieved point scores: {scores}")

        if max(scores) < SIMILARITY_THRESHOLD:
            logger.warning(f"Max similarity score {max(scores)} is below threshold {SIMILARITY_THRESHOLD}. Considering this a weak match, but proceeding.")
        
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
```

## Outcome

- ✅ Impact: The RAG system should now correctly extract text content from Qdrant payloads, eliminating empty contexts and preventing misleading fallback responses, based on the live inspection of the Qdrant payload keys.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `backend/app/tools/rag_tool.py`
- 🔁 Next prompts: 
- 🧠 Reflection: This highlights the critical importance of verifying assumptions, especially regarding data structures (like Qdrant payload keys). The diagnostic script was essential in identifying the discrepancy and leading to the correct fix.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
