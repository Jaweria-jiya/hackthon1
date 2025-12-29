```python
async def retrieve_from_book(query: str, top_k: int = 5) -> str:
    """
    Retrieves context from Qdrant by explicitly generating embeddings with OpenAI
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
            if hit.payload and 'page_content' in hit.payload:
                context += hit.payload['page_content'] + "\n\n"
                logger.debug(f"Retrieved chunk ID: {hit.id}, score: {hit.score}, text: {hit.payload['page_content'][:100]}...")
        
        final_decision = f"Retrieved {len(retrieved_points.points)} documents from Qdrant successfully."
        logger.info(f"✅ Final retrieval decision: {final_decision}")
        return context.strip()

    except Exception as e:
        logger.error(f"ERROR: Qdrant retrieval failed during query for query '{query}': {e}", exc_info=True)
        raise RetrievalError(f"Qdrant retrieval failed: {e}") from e
```