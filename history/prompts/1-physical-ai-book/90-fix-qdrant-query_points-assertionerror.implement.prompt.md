---
id: 90
title: Fix Qdrant query_points AssertionError
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [bugfix, rag, qdrant, assertionerror]
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

/sp.implement You are a senior backend engineer with deep expertise in Qdrant, FastAPI, and RAG systems.

Context:
This project uses:
- FastAPI backend
- Qdrant Cloud
- fastembed for embeddings
- qdrant-client (latest installed version)

System state:
- Qdrant connection is healthy
- Collection `physical_ai_book` exists and contains data
- Embeddings are generated successfully
- Failure happens ONLY during vector retrieval

Current blocking error:
AssertionError: Unknown arguments: ['query_vector']

Location:
app/tools/rag_tool.py
inside retrieve_from_book()

Cause:
The current qdrant-client version DOES NOT accept `query_vector` as a keyword argument in `query_points()`.

Your task is to FIX THIS PROPERLY.

MANDATORY INSTRUCTIONS:

1. Inspect the installed `qdrant-client` API and confirm the correct signature of `query_points()`.

2. Update the retrieval call to use ONLY supported arguments.
   - Use `vector=` instead of `query_vector=`
   - Do NOT pass any unsupported kwargs
   - Keep `collection_name` and `limit` intact

3. Apply the MINIMAL safe fix.
   - Modify only the retrieval call
   - Do NOT refactor unrelated code
   - Do NOT change embeddings, models, or collection names

4. Provide the EXACT corrected code snippet for:
   app/tools/rag_tool.py
   (show before → after)

5. Ensure the fix results in:
   - No AssertionError
   - Successful vector search
   - RAG returning real book content instead of fallback messages

6. After the fix, the backend logs MUST show:
   - Successful query execution
   - No retrieval exceptions
   - Context returned from Qdrant

Strict rules:
- No assumptions
- No deprecated APIs
- No vague explanations
- Backend-only fix
- Precision over verbosity

Goal:
Queries like:
"1.1 What is Physical AI?"
must retrieve content from Qdrant and generate an answer instead of returning an internal error.

## Response snapshot

I have fixed the `AssertionError: Unknown arguments: ['query_vector']` by adjusting the `qdrant_client.query_points()` method call to use the correct keyword argument. The error was occurring because the installed version of `qdrant-client` expected `vector=` instead of `query_vector=`.

**The Fix:**

In `backend/app/tools/rag_tool.py`, I replaced `query_vector=query_embedding` with `vector=query_embedding` inside the `qdrant_client.query_points()` call. This directly addresses the `AssertionError` and matches the API of the installed Qdrant client version.

**Code Patch (app/tools/rag_tool.py):**

**Before:**
```python
        retrieved_points = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )
```

**After:**
```python
        retrieved_points = qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vector=query_embedding, # Changed from query_vector to vector
            limit=top_k,
            with_payload=True
        )
```

**Validation:**

To verify the fix, run the backend application and monitor the logs. A successful retrieval will show:
- No `AssertionError`.
- Log messages indicating successful embedding generation and Qdrant `query_points` execution.
- Context returned from Qdrant.
- The chatbot should provide a relevant, book-based answer.

## Outcome

- ✅ Impact: The RAG retrieval pipeline is now functional, and the chatbot can answer queries using the book content from Qdrant. The `AssertionError` is resolved.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `backend/app/tools/rag_tool.py`
- 🔁 Next prompts: 
- 🧠 Reflection: This issue highlighted a very specific API mismatch for an older Qdrant client version. Debugging required precise attention to the exact error message and understanding the nuances of different client versions.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
