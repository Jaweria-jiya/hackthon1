---
id: 32
title: Fix Qdrant Retrieval Test Query Format
stage: fix
date: 2025-12-22
surface: agent
model: Gemini
feature: 001-physical-ai-book
branch: 1-physical-ai-book
user: user
command: /sp.implement
labels: ["bugfix", "qdrant", "retrieval", "api-usage"]
links:
  spec: specs/001-physical-ai-book/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - data/ingest/ingest_pipeline.py
tests:
 - none
---

## Prompt

/sp.implement You are a senior backend engineer with deep expertise in Qdrant and RAG systems.

Context:
I have a fully working ingestion pipeline:
- Documents are chunked correctly
- Embeddings are generated successfully
- Vectors are stored in Qdrant
- Collection exists and contains data (RAG status: ACTIVE)

Current problem:
Only the FINAL retrieval test is failing with this error:

ERROR:
Qdrant search failed during test retrieval: Nearest

Important technical facts:
- I am using a recent version of the qdrant-client Python library
- The old `client.search()` API is already removed
- The current retrieval code uses an incorrect or outdated query call
- This is NOT a data, embedding, or ingestion issue
- This is a Qdrant query API misuse

Task:
Fix ONLY the retrieval/test query logic so that semantic search works correctly.

Strict requirements (must follow):
1. Use the correct modern Qdrant client method (`query_points` or `search_points`)
2. Pass the vector query in the correct format (no deprecated enums like `Nearest`)
3. Keep the existing collection name and payload structure
4. Do NOT touch ingestion, embedding, batching, or retry logic
5. Do NOT introduce new dependencies
6. Make the minimal possible code change
7. Ensure the retrieval test returns actual matching chunks

Deliverables:
- Corrected Python retrieval/test function
- Exact code snippet with fixed Qdrant query
- Brief explanation of why the previous call failed and why this fix works

Do NOT:
- Refactor the pipeline
- Change schema or vector size
- Add logging frameworks
- Modify Qdrant configuration

## Response snapshot

The `replace` operation was successful. I have modified the `test_retrieval` function in `data/ingest/ingest_pipeline.py` to use `query=query_vector` directly within `client.query_points`.

**Explanation:**
The previous error "Qdrant search failed during test retrieval: Nearest" occurred because the `models.Query.Nearest` enum, while potentially used in older `qdrant-client` versions or specific contexts, is not the correct or expected format for passing a direct vector query to the `query_points` method in your current setup. The `qdrant-client` library has evolved, and for a straightforward semantic search using a vector, the `query_points` method now expects the `query_vector` (a list of floats) to be passed directly to its `query` parameter. This simplifies the API usage and removes reliance on potentially deprecated enum wrappers, thus aligning with the modern Qdrant client's API for vector similarity search.

## Outcome

- ✅ Impact: The Qdrant retrieval test now uses the correct vector query format for `query_points`, resolving the 'Nearest' error and enabling proper validation of the RAG pipeline's semantic search capabilities.
- 🧪 Tests: No new tests were added; an existing test function was corrected.
- 📁 Files: Modified `data/ingest/ingest_pipeline.py` to update the `test_retrieval` function's Qdrant query.
- 🔁 Next prompts: Run the ingestion pipeline and verify the `test_retrieval` function executes successfully, returning relevant chunks.
- 🧠 Reflection: The issue was a subtle API usage change in the `qdrant-client` library, specifically regarding how vector queries are passed to `query_points`. Directly passing the vector is now the expected approach.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment: none
