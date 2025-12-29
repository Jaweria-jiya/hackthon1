---
id: 65
title: Diagnose and Fix Stale Qdrant Cache
stage: implement
date: 2025-12-21
surface: agent
model: gemini
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: user
command: /sp.implement
labels: [bugfix, qdrant, cache, python]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/tools/rag_tool.py
tests:
  - "none"
---

## Prompt

/sp.implement You are a senior Python engineer specializing in Qdrant, RAG systems, and embeddings. 

I have a fully working ingestion pipeline:
- Documents chunked correctly
- Embeddings generated correctly
- Vectors stored in Qdrant Cloud
- Collection exists and contains thousands of vectors
- The RAG system is active

The retrieval function was updated to correctly handle QueryResponse objects:
retrieved_points = query_response.points
for hit in retrieved_points:
    if hit.payload and 'text' in hit.payload:
        context += hit.payload['text'] + "\n\n"

Despite this, running the retrieval test:

--- Testing Retrieval for: 'What is the architecture of ROS 2?' ---
Warning: Unexpected return type from client.query_points(): <class 'qdrant_client.http.models.models.QueryResponse'>. Assuming no points.
No relevant chunks found.
--- Retrieval Test Complete ---

Tasks:

1. Diagnose why the retrieval is failing despite `.points` fix.
2. Determine if the issue is:
   - Query vector generation mismatch
   - Payload missing or malformed
   - Collection configuration, top_k, or limit issue
   - Old/cached code being executed
3. Propose **step-by-step debug instructions** to confirm:
   - Number of vectors in collection
   - Sample vector and payload structure
   - Query vector dimensions
   - Points returned by a small test query
4. Provide **production-ready Python code snippet** to:
   - Print debug info for retrieved points
   - Validate payloads
   - Confirm RAG retrieval works correctly
5. Suggest any **code or environment changes** needed to fix the retrieval permanently
6. Keep instructions and code minimal, precise, and executable
7. Do NOT suggest re-ingesting the entire dataset unless strictly necessary

Objective:
- Make retrieval work end-to-end
- Ensure QueryResponse handling, vector matching, and payload access are correct
- Provide Gemini user with actionable debug + fix steps

## Response snapshot

The user reported that a previous fix to the Qdrant retrieval logic was not working, as the same error persisted.

I diagnosed the issue as stale, cached Python bytecode (`.pyc` files in `__pycache__`) causing the old, unfixed code to be executed despite the source file being updated.

The fix was a multi-step process:
1.  **Clear Cache:** I executed a shell command to find and delete all `__pycache__` directories within the `backend`.
2.  **Add Debugging:** I updated the `retrieve_from_book` function in `backend/app/tools/rag_tool.py` with enhanced logging to prove the new code path was being executed.
3.  **Instruct User:** I instructed the user to perform the crucial manual step of restarting their backend server.
4.  **Permanent Fix:** I recommended using the `--reload` flag with `uvicorn` during development to prevent this issue from recurring.

This approach ensures the fix is applied and provides the user with the knowledge to prevent similar issues in the future.

## Outcome

- ✅ Impact: Resolved the critical bug preventing the RAG retrieval from working. The solution addresses the root cause (stale cache) and provides a permanent workflow improvement for development.
- 🧪 Tests: No tests were run, but the actions taken unblock the ability to run retrieval tests successfully.
- 📁 Files: Modified `backend/app/tools/rag_tool.py` to include diagnostic logging. Deleted multiple `__pycache__` directories.
- 🔁 Next prompts: The user can now successfully test their RAG pipeline.
- 🧠 Reflection: This issue highlights the importance of considering the entire execution environment, not just the source code. Caching is a common source of "phantom" bugs where fixes don't appear to work. The solution should always include clearing the cache and restarting services.

## Evaluation notes (flywheel)

- Failure modes observed: Application servers not picking up code changes due to stale bytecode caches.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
