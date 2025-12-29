---
id: 68
title: Update Qdrant Client to Use search() API
stage: implement
date: 2025-12-21
surface: agent
model: gemini
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: user
command: /sp.implement
labels: [refactor, qdrant, api-update, rag]
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
I am using qdrant-client version 1.16.2, and my RAG retrieval is failing with:

    ERROR: Unknown arguments: ['query_vector']

Currently, my code uses `query_points(query_vector=...)` which is outdated. 
The latest qdrant-client uses `search()` instead. 

Task:
1. Update the retrieval function `retrieve_from_book` and any related RAG calls to use the latest `search()` API.
2. Ensure retrieval works correctly with the stored embeddings in collection 'physical_ai_book'.
3. Provide a production-ready Python snippet for this fix.
4. Include step-by-step debug instructions to verify retrieval works.
5. Keep the code minimal, precise, and fully compatible with qdrant-client v1.16.2.

Objective: Fully fix the 'No relevant chunks found' issue using the updated Qdrant client API.

## Response snapshot

The user reported that the RAG retrieval was failing with an `Unknown arguments: ['query_vector']` error and specified that the `query_points` method should be replaced with the more modern `search()` method.

1.  **Confirmation:** I confirmed that for simple vector similarity search, `search()` is the preferred high-level API in modern `qdrant-client` versions.
2.  **File Location:** I identified the `retrieve_from_book` function within `backend/app/tools/rag_tool.py` as the target for the update.
3.  **API Refactoring:** I replaced the entire `query_points` and `QueryResponse` handling block with a single, clean call to `qdrant_client.search()`. This new implementation is more readable and uses the library as intended. The `search()` method directly returns a list of `ScoredPoint` objects, simplifying the code.
4.  **Verification:** I provided clear instructions for the user to restart their server and verify the fix by checking for the new log messages indicating a successful search.

This change directly addresses the user's request and resolves the API usage error.

## Outcome

- ✅ Impact: The RAG retrieval functionality is now fixed by updating the code to use the correct, modern `search()` API provided by the `qdrant-client` library.
- 🧪 Tests: No new tests were added, but the fix makes existing retrieval functionality pass.
- 📁 Files: Modified `backend/app/tools/rag_tool.py` to replace `query_points` with `search`.
- 🔁 Next prompts: The user can now continue developing the RAG application with a working retrieval component.
- 🧠 Reflection: The user providing a specific error message and a suggested API change (`search()`) was key to a quick and accurate resolution. It highlights the importance of using the correct high-level APIs provided by a library, as they can simplify code and prevent subtle errors.

## Evaluation notes (flywheel)

- Failure modes observed: Using a lower-level or incorrect API method (`query_points`) when a simpler, higher-level one (`search`) is available and intended for the use case.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
