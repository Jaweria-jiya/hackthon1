def retrieve_from_book(query: str, top_k: int = 5) -> str:
    """
    Retrieves context from Qdrant by explicitly generating embeddings with FastEmbed
    and using the qdrant_client.query_points() method.
    """
    if not RAG_ENABLED or not qdrant_client or not embedding_model:
        logger.warning("RAG is disabled or not configured. Skipping retrieval.")
        return ""  # Fail-safe: return empty context if RAG is not working

    try:
        original_query = query
        normalized_query = _normalize_query(original_query)
        logger.info(f"Original query: '{original_query}', Normalized query: '{normalized_query}'")

        # Generate embedding explicitly with FastEmbed
        logger.info("Generating embedding with FastEmbed...")
        query_embedding = list(embedding_model.embed([normalized_query]))[0]
        logger.info("✅ Embedding generated successfully.")
        
        logger.info(f"Searching collection '{settings.QDRANT_COLLECTION_NAME}' with top_k={top_k}")

        # Use the correct `query_points` method with a list of floats for the query
        retrieved_points = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query=query_embedding.tolist(), # Changed to pass list of floats directly
            limit=top_k,
            with_payload=True
        )
        logger.info(f"Qdrant query_points returned {len(retrieved_points)} points.")

        if not retrieved_points:
            logger.warning("No matching documents found in Qdrant. Final decision: No context.")
            return ""

        # Log scores for debugging
        scores = [hit.score for hit in retrieved_points]
        logger.info(f"Retrieved point scores: {scores}")

        # Basic thresholding to relax retrieval
        if max(scores) < SIMILARITY_THRESHOLD:
            logger.warning(f"Max similarity score {max(scores)} is below threshold {SIMILARITY_THRESHOLD}. Considering this a weak match, but proceeding.")
            # Even if it's a weak match, we proceed as per the "Relaxed Threshold" requirement
        
        context = ""
        retrieved_ids = [hit.id for hit in retrieved_points]
        logger.info(f"Retrieved point IDs: {retrieved_ids}")

        for hit in retrieved_points: 
            if hit.payload and 'text' in hit.payload:
                context += hit.payload['text'] + "\n\n"
                logger.debug(f"Retrieved chunk ID: {hit.id}, score: {hit.score}, text: {hit.payload['text'][:100]}...")
        
        final_decision = f"Retrieved {len(retrieved_points)} documents from Qdrant successfully."
        logger.info(f"✅ Final retrieval decision: {final_decision}")
        return context.strip()

    except Exception as e:
        logger.error(f"ERROR: Qdrant retrieval failed during query for query '{query}': {e}", exc_info=True)
        raise RetrievalError(f"Qdrant retrieval failed: {e}") from e
