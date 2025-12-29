---
id: 59
title: Refactor from OpenRouter to OpenAI & Debug Qdrant URL
stage: implement
date: 2025-12-19
surface: agent
model: gemini-pro
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: ALI
command: /sp.implement
labels: [refactor, openrouter, openai, qdrant, debug, failure]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- backend/app/core/gemini.py
- backend/app/agents/book_rag_agent.py
- data/ingest/ingest_pipeline.py
- FINAL_STATUS_REPORT.md
tests:
[]
---

## Prompt

/sp.implement

You are a senior production backend engineer working on a live RAG system.

======================
CRITICAL CONTEXT
======================

The project previously used OPENROUTER_API_KEY.
This variable NO LONGER EXISTS.

✅ The ONLY valid API key is:
   OPENAI_API_KEY

✅ It is already defined in:
   backend/.env

❌ You are STRICTLY FORBIDDEN from:
   - Using OPENAIROUTER_API_KEY anywhere
   - Using localhost Qdrant
   - Creating, editing, deleting, or guessing any .env file
   - Falling back to default values
   - Creating or recreating any Qdrant collection

👉 backend/.env is the SINGLE source of truth.
👉 All credentials already exist and are valid.

======================
MANDATORY GLOBAL REFACTOR
======================

1️⃣ Scan the ENTIRE backend folder:

backend/

2️⃣ Replace EVERY occurrence of:
- OPENAIROUTER_API_KEY
- openrouter clients
- openrouter headers
- openrouter model prefixes (e.g. openai/gpt-4o-mini)

WITH:
- OPENAI_API_KEY
- Official OpenAI client
- Standard OpenAI models (e.g. gpt-4o-mini)
- No extra router headers

This includes (but is not limited to):
- agents
- services
- ingestion
- embeddings
- RAG logic

======================
ENV LOADING (STRICT)
======================

Modify `data/ingest/ingest_pipeline.py` so that:

- dotenv is loaded EXPLICITLY from backend/.env
- No other .env path is allowed

MANDATORY logic:

backend_env_path = os.path.join(PROJECT_ROOT, "backend", ".env")
load_dotenv(backend_env_path)

Before connecting:
- Print the resolved QDRANT_URL
- If it contains "localhost" → ABORT immediately

======================
QDRANT RULES (NON-NEGOTIABLE)
======================

- Qdrant is CLOUD (HTTPS)
- Collection `physical_ai_book` ALREADY EXISTS
- DO NOT create, recreate, delete, or modify the collection

If collection does NOT exist:
❌ STOP execution
❌ Report failure

======================
INGESTION TASK
======================

- Use OPENAI_API_KEY for embeddings (3072-dim)
- Connect to Qdrant using QDRANT_URL and QDRANT_API_KEY
- Upsert into existing collection only
- Run one similarity search
- Confirm points count > 0

======================
FINAL OUTPUT REQUIRED
======================

Report clearly:
- API key used (OPENAI_API_KEY)
- QDRANT_URL used
- Collection name
- Total vectors in Qdrant
- RAG status: ACTIVE or FAILED

======================
ABSOLUTE RULES
======================

- NO OPENAIROUTER_API_KEY
- NO localhost
- NO env guessing
- NO env deletion
- NO collection creation

======================
GOAL
======================

Completely remove OpenRouter,
standardize the backend on OPENAI_API_KEY,
successfully connect to Cloud Qdrant,
and activate the RAG system without any manual fixes.

## Response snapshot

# Final Status Report

**Ingestion Status:** FAILED

**Summary:**
The Qdrant ingestion process could not be completed. The codebase was successfully refactored to remove all `openrouter` references and standardize on the official OpenAI API. The `ingest_pipeline.py` script was correctly configured to load environment variables from `backend/.env` and enforce all user-defined constraints. However, the process failed due to an invalid Qdrant URL provided in the `backend/.env` file.

**Execution Details:**
- **Codebase Refactoring:**
    - `backend/app/core/gemini.py`: Log message updated to reflect Gemini usage.
    - `backend/app/agents/book_rag_agent.py`: All `openrouter` client, model, and API key references were successfully replaced with official OpenAI API usage.
- **Ingestion Pipeline Execution:**
    - The `data/ingest/ingest_pipeline.py` script was executed.
    - It correctly loaded the `backend/.env` file.
    - It resolved `QDRANT_URL` to `http://localhost:6333`.
    - As per strict user instructions ("If it contains "localhost" → ABORT immediately"), the script aborted execution with the message: `FATAL: QDRANT_URL points to localhost. Aborting.`.
- **Root Cause:** The `QDRANT_URL` variable in the `backend/.env` file is set to a `localhost` address, which directly violates the user's critical instruction that "Qdrant is CLOUD (HTTPS)" and that "NO localhost" connections are allowed.
- **Blocking Issue:** I am strictly forbidden from creating, editing, deleting, or guessing any `.env` file, and I am also unable to inspect the contents of `backend/.env` due to file ignore patterns. Therefore, I cannot programmatically correct the invalid `QDRANT_URL` or verify other credentials.

**Conclusion:**
The RAG system is **NOT ACTIVE**. Despite successful refactoring and strict adherence to all rules, the ingestion pipeline is blocked by an invalid `QDRANT_URL` specified in `backend/.env`, which I am unable to rectify.

**Next Steps (Informational):**
To resolve this issue, the user **must manually correct** the `QDRANT_URL` variable in the `backend/.env` file to point to the actual cloud-based Qdrant instance URL (e.g., `https://[your-qdrant-cluster-id].qdrant.tech`) and ensure all other credentials are valid. Once the `backend/.env` is correctly configured, the ingestion pipeline can be re-executed.

## Outcome

- ✅ Impact: All `openrouter` references were successfully removed from the backend codebase. The ingestion pipeline now correctly attempts to use the official OpenAI API and load credentials from `backend/.env`. The root cause of the Qdrant connection failure (localhost URL in `backend/.env`) was identified and reported.
- 🧪 Tests: The ingestion pipeline script includes built-in verification steps, but these could not be fully executed due to the Qdrant connection failure.
- 📁 Files:
  - `backend/app/core/gemini.py`: Modified.
  - `backend/app/agents/book_rag_agent.py`: Modified.
  - `data/ingest/ingest_pipeline.py`: Modified.
  - `FINAL_STATUS_REPORT.md`: Created.
- 🔁 Next prompts: The user needs to manually correct the `QDRANT_URL` in `backend/.env` to a valid cloud address.
- 🧠 Reflection: Strict constraints regarding `.env` file access and modification, combined with an invalid initial configuration, led to a programmatic impasse. The solution required detailed error reporting and clear instructions for manual user intervention.

## Evaluation notes (flywheel)

- Failure modes observed: Inability to programmatically inspect or modify a critical configuration file (`backend/.env`) due to ignore rules, leading to an unresolvable execution block despite correct code logic.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
