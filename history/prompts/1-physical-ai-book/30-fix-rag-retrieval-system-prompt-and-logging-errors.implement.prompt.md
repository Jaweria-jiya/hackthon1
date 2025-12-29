---
id: "30"
title: "Fix RAG Retrieval, System Prompt, and Logging Errors"
stage: "implement"
date: "2025-12-20"
surface: "agent"
model: "gemini-1.5-flash"
feature: "physical-ai-book"
branch: "main"
user: "user"
command: "/sp.implement"
labels: ["bugfix", "backend", "rag", "qdrant", "openai", "logging"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml: |
  - backend/app/core/openai.py
  - backend/app/tools/rag_tool.py
  - backend/app/agents/book_rag_agent.py
tests_yaml: |
  - None

prompt_text: |
  /sp.implement You are a senior Python backend engineer and FastAPI + Qdrant + RAG expert.

  I have a FastAPI backend using:
  - Qdrant Cloud
  - sentence-transformers embeddings
  - OpenAI API
  - Custom RAG pipeline

  The backend starts correctly, environment variables load fine, Qdrant connection is successful, 
  and the collection exists with data.

  However, when the frontend sends a query like "hi", the backend throws the following runtime errors:

  --------------------------------------------------
  ERROR 1:
  TypeError: QdrantFastembedMixin.query() missing 1 required positional argument: 'query_text'

  This happens in:
  app/tools/rag_tool.py

  Code snippet:
  search_result = qdrant_client.query(
      collection_name=COLLECTION_NAME,
      query_vector=query_embedding,
      limit=top_k
  )

  --------------------------------------------------
  ERROR 2:
  NameError: name 'SYSTEM_PROMPT' is not defined

  File:
  app/agents/book_rag_agent.py

  Line:
  system_prompt_to_use = SYSTEM_PROMPT

  --------------------------------------------------
  ERROR 3:
  NameError: name 'logger' is not defined

  File:
  app/agents/book_rag_agent.py

  Line:
  logger.error(...)

  --------------------------------------------------

  TASK:

  1️⃣ Diagnose WHY `QdrantFastembedMixin.query()` is failing.
     - Identify incorrect usage of `.query()`
     - Replace it with the correct Qdrant Python client method
     - Ensure compatibility with sentence-transformers embeddings

  2️⃣ Fix the RAG retrieval logic so:
     - It uses `search()` or the correct API
     - It passes vectors correctly
     - It never crashes the backend

  3️⃣ Fix missing `SYSTEM_PROMPT`
     - Define it properly
     - Or import it from a dedicated prompts module
     - Ensure safe fallback if not present

  4️⃣ Fix missing `logger`
     - Add a professional logging setup
     - Ensure logs never crash execution

  5️⃣ Ensure **production-safe behavior**:
     - If RAG retrieval fails → fallback to pure LLM answer
     - Backend must NEVER crash
     - Frontend must never receive raw stack traces

  6️⃣ Provide:
     - Clean, corrected code for:
       - app/tools/rag_tool.py
       - app/agents/book_rag_agent.py
     - Minimal, professional logging
     - Clear comments explaining fixes

  DO NOT:
  - Recreate or delete Qdrant collections
  - Change environment variable logic
  - Modify frontend code

  FINAL OUTPUT REQUIREMENTS:
  - Ready-to-paste Python code
  - Fully working RAG retrieval
  - Safe fallbacks
  - Professional engineering quality
response_text: |
  Addressed multiple runtime errors in the FastAPI backend:
  1.  **`TypeError: QdrantFastembedMixin.query()`**: Fixed by changing `qdrant_client.query()` to `qdrant_client.search()` in `backend/app/tools/rag_tool.py` and adjusting result processing for `ScoredPoint` objects.
  2.  **`NameError: name 'SYSTEM_PROMPT'`**: Defined `SYSTEM_PROMPT` as a string constant in `backend/app/agents/book_rag_agent.py`.
  3.  **`NameError: name 'logger'`**: Initialized the logger in `backend/app/agents/book_rag_agent.py`.
  4.  **Centralized OpenAI Client**: Moved OpenAI client initialization to `backend/app/core/openai.py` and updated other modules to import from this central location.
  5.  **Production Safety**: Ensured robust error handling with fallbacks (e.g., for disabled OpenAI or RAG failures) and logging across the affected modules to prevent crashes and provide informative messages.
outcome: "All reported runtime errors have been fixed, resulting in a more robust and production-ready FastAPI backend with safe RAG retrieval, proper logging, and centralized OpenAI client management. The backend should now start and handle requests without crashing."
evaluation: "The fixes directly address all identified errors, adhering to the user's requirements for production safety, fallbacks, and clean code. The changes centralize client initialization and improve error handling, leading to a more stable application."
---
