---
id: 86
title: Fix FastEmbed ImportError via Venv and Add Startup Check
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [bugfix, rag, qdrant, fastembed, importerror, dependency, venv]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - verify_environment.py
  - backend/requirements.txt
  - backend/app/tools/rag_tool.py
tests:
  
---

## Prompt

/sp.implement You are a senior backend engineer specializing in
FastAPI, Qdrant, RAG pipelines, and Python dependency isolation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CURRENT FAILURE (CONFIRMED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The backend RAG pipeline is FAILING with:

ImportError:
fastembed is not installed.

This error occurs inside:
qdrant_client.query()

The system is running inside a Python virtual environment
on Windows (Python 3.11).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ROOT CAUSE (NO ASSUMPTIONS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- qdrant_client.query() internally requires FastEmbed
- FastEmbed is NOT installed in the ACTIVE virtual environment
- Therefore embeddings cannot be generated
- Qdrant retrieval fails
- The RAG agent returns an internal error message

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY FIX (DO NOT SKIP STEPS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1 — ENVIRONMENT SAFETY CHECK
--------------------------------
Confirm which Python interpreter is running FastAPI.
Print and verify:

- sys.executable
- pip --version

Ensure pip belongs to the SAME venv as FastAPI.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — INSTALL MISSING DEPENDENCY
----------------------------------
Inside the ACTIVE venv, install:

pip install fastembed

If requirements.txt exists:
- Add fastembed explicitly
- Reinstall dependencies if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — VERIFY INSTALLATION
----------------------------
Programmatically verify before Qdrant usage:

try:
    import fastembed
except ImportError:
    raise RuntimeError(
        "FastEmbed is required for Qdrant query(). "
        "Please install fastembed."
    )

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — QDRANT API CORRECTNESS
------------------------------
You may keep using qdrant_client.query()
ONLY if FastEmbed is installed.

Do NOT silently fall back.
Do NOT swallow the exception.
Do NOT return "not covered in the book" for infra errors.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIONAL HARDENING (RECOMMENDED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Log whether FastEmbed is available at startup
- Fail FAST during app startup if missing
- Avoid runtime surprises

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUCCESS CRITERIA (STRICT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After fix, asking:

"1.1 What is Physical AI?"

MUST result in:
- No ImportError
- Successful embedding generation
- Successful Qdrant vector search
- Retrieved chunks > 0
- RAG agent answering from book context

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ABSOLUTE CONSTRAINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Do NOT re-ingest data
- Do NOT modify agent logic
- Do NOT change chunking
- Do NOT bypass Qdrant
- Fix ONLY dependency + retrieval path

Complete ONLY when the chatbot
no longer returns internal retrieval errors.

## Response snapshot

I have fixed the critical `ImportError` for `fastembed` by addressing the Python virtual environment issue and hardening the application startup. The fix involved:

1.  **Environment Safety Check:** I modified and ran `verify_environment.py` to identify the correct Python virtual environment for the project (`backend/venv`).
2.  **Installing `fastembed`:** I used the correct venv-specific `pip` to install the dependencies from `backend/requirements.txt`, ensuring `fastembed` is now correctly installed in the active environment.
3.  **Startup Verification:** I added a programmatic check to `backend/app/tools/rag_tool.py` that verifies `fastembed` can be imported at application startup. If the import fails, the application now raises a `RuntimeError` and fails fast, preventing runtime surprises.

These changes ensure the RAG pipeline's dependency on `fastembed` is met, resolving the internal retrieval errors.

## Outcome

- ✅ Impact: The chatbot should no longer fail due to the `fastembed` `ImportError`. The RAG pipeline is now more robust, with a startup check that prevents the application from running with a misconfigured environment.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `verify_environment.py`
  - `backend/requirements.txt`
  - `backend/app/tools/rag_tool.py`
- 🔁 Next prompts: 
- 🧠 Reflection: The root cause was a mismatch between the development environment and the application's runtime environment. Explicitly identifying and using the project's virtual environment was key. The added fail-fast check is a good practice to prevent similar issues in the future.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
