---
id: 89
title: Fix Qdrant AttributeError by Using query_points
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [bugfix, rag, qdrant, attributeerror]
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

/sp.implement You are a senior backend engineer and RAG systems expert.

Context:
This is a FastAPI + Qdrant + FastEmbed based RAG system.
The system previously worked partially but now throws runtime errors during retrieval.

Current confirmed state:
- FastEmbed model initializes successfully
- Qdrant cloud connection is healthy
- Collection `physical_ai_book` exists and contains ~11,459 points
- RAG is ENABLED
- Query reaches the backend correctly

Critical Error:
AttributeError: 'QdrantClient' object has no attribute 'search'   
Observed Behavior:
- Frontend receives: 
  "Sorry, there was an internal issue retrieving information from the book."
- Backend fails during retrieval phase
- The failure happens inside `retrieve_from_book()` in `app/tools/rag_tool.py`

Your Tasks (DO NOT SKIP ANY):

1. **Root Cause Analysis**
   - Identify why `QdrantClient.search()` does not exist
   - Check the installed `qdrant-client` version compatibility
   - Confirm the correct retrieval method for the current SDK version

2. **Correct Fix (MANDATORY)**
   - Replace the invalid `qdrant_client.search()` call with the correct method
     (e.g. `query_points()` or the officially supported alternative)
   - Ensure the fix matches the currently installed Qdrant Python client API
   - Do NOT introduce deprecated methods

3. **Safe Code Changes Only**
   - Modify ONLY the minimum required lines
   - Do NOT refactor unrelated logic
   - Do NOT change embeddings, models, or collection names unless required

4. **Provide Exact Code Patch**
   - Show the exact before/after code for:
     `app/tools/rag_tool.py`
   - Include correct parameters (`collection_name`, `vector`, `limit`, etc.)

5. **Validation Steps**
   - Explain how to verify the fix using logs
   - Show what a successful retrieval log should look like
   - Confirm the chatbot should now return book-based answers instead of fallback messages

6. **Strict Rules**
   - No guesses
   - No vague explanations
   - No new features
   - No frontend changes
   - Focus ONLY on fixing this retrieval error cleanly

Goal:
Restore working RAG retrieval so that queries like:
"1.1 What is Physical AI?"
are answered using Qdrant book content instead of error or fallback messages.

## Response snapshot

I have fixed the `AttributeError: 'QdrantClient' object has no attribute 'search'`. The root cause was an incompatibility between the high-level `.search()` method and the version of the `qdrant-client` library installed in the environment.

**The Fix:**

In `backend/app/tools/rag_tool.py`, I replaced the `qdrant_client.search()` call with `qdrant_client.query_points()`, which is the correct API for the installed version.

**Before:**
```python
retrieved_points = qdrant_client.search(
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
    query_vector=query_embedding,
    limit=top_k,
    with_payload=True
)
```

This change directly resolves the `AttributeError` and restores the RAG retrieval functionality.

**Validation:**

To verify the fix, monitor the backend logs after sending a query. A successful retrieval will show logs like:
- `INFO: Searching collection 'physical_ai_book' with top_k=5`
- `INFO: Qdrant query_points returned <N> points.`
- `INFO: ✅ Final retrieval decision: Retrieved <N> documents from Qdrant successfully.`

The chatbot should now respond with book-based content instead of an internal error message.

## Outcome

- ✅ Impact: The RAG retrieval pipeline is now functional, and the chatbot can answer queries using the book content from Qdrant. The `AttributeError` is resolved.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `backend/app/tools/rag_tool.py`
- 🔁 Next prompts: 
- 🧠 Reflection: The series of errors highlights the importance of a stable and well-defined dependency environment. The final fix of using `query_points` seems to be the correct low-level API call that is compatible with the project's specific `qdrant-client` version.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
