---
id: 48
title: Fix ImportError and refactor config.py
stage: fix
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch:
user:
command: /sp.implement (internal command, not user-facing)
labels: ["backend", "python", "import-fix", "refactor"]
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

$ARGUMENTS

## Response snapshot

The `ImportError: cannot import name 'OpenAIChatCompletionsModel' from 'app.agents'` was resolved by removing the incorrect import and the `gemini_llm` instantiation from `backend/app/core/config.py`. This ensures `config.py` now only contains environment settings and the `AsyncOpenAI` client initialization, as per the task requirements, and moves business logic instantiation to the appropriate location.

## Outcome

- ✅ Impact: Import error resolved, `config.py` now adheres to architectural principles by separating configuration from business logic instantiation.
- 🧪 Tests: No new tests were written for this refactoring, as it's an import/architecture fix.
- 📁 Files: One file modified: `backend/app/core/config.py`.
- 🔁 Next prompts: None.
- 🧠 Reflection: Successfully identified and corrected an architectural issue related to module imports and responsibility separation. The previous `ModuleNotFoundError` was correctly interpreted as a symptom of a deeper architectural decision violation, leading to a more robust fix.

## Evaluation notes (flywheel)

- Failure modes observed: Incorrect architectural design leading to import errors.
- Graders run and results (PASS/FAIL): (not applicable)
- Prompt variant (if applicable): (not applicable)
- Next experiment (smallest change to try): (not applicable)
