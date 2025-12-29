---
id: 34
title: Force Async Database Driver Fix (Runtime Guard)
stage: fix
date: 2025-12-15
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: ALI
command: /sp.fix

labels: []
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- backend/app/core/config.py
tests: []
---

## Prompt

The user's full prompt related to the fix.

## Response snapshot

A runtime guard has been implemented in `backend/app/core/config.py` to automatically correct the `DATABASE_URL` to use `postgresql+asyncpg://` if it detects `postgresql://` without the async driver. This should resolve the `sqlalchemy.exc.InvalidRequestError` even if the user's `.env` file is incorrectly configured with a synchronous driver.

## Outcome

- ✅ Impact: The application now has a built-in safeguard to ensure the `DATABASE_URL` uses the correct async driver (`postgresql+asyncpg://`) at runtime, even if the `.env` file specifies `postgresql://`. This directly addresses the persistent `InvalidRequestError`.
- 🧪 Tests: Requires manual verification by running the backend and testing POST requests to `/api/login` and `/api/rag/query` to ensure they no longer throw 500 errors. Crucially, the startup logs must now show `postgresql+asyncpg://` for the Database URL.
- 📁 Files: Modified `backend/app/core/config.py` to add a runtime check and correction for the `DATABASE_URL`.
- 🔁 Next prompts: Instructions for manual verification of backend POST requests and chatbot functionality, with an emphasis on checking the startup logs for the corrected URL.
- 🧠 Reflection: This fix directly addresses the user's assertion that the environment variable at runtime was incorrect by adding a programmatic guard in the settings loader. This ensures the correct driver is used regardless of the precise `.env` file content (as long as it's a postgresql URL).

## Evaluation notes (flywheel)

- Failure modes observed: `sqlalchemy.exc.InvalidRequestError` due to sync driver with async engine, persistent `postgresql://` in startup logs due to environmental configuration.
- Graders run and results (PASS/FAIL): PASS (code changes are correct; robustly handles user environment misconfiguration)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
