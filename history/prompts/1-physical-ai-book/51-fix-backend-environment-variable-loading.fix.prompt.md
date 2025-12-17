---
id: 51
title: Fix Backend Environment Variable Loading
stage: fix
date: 2025-12-17
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: main
user: ALI
command: |
  /sp.implement You are acting as a Principal Backend Infrastructure Engineer.

  CRITICAL ISSUE:
  The backend is crashing due to inconsistent environment variable loading.
  Pydantic Settings is detecting:
  - Missing required variable: QDRANT_HOST
  - Unexpected extra variable: qdrant_url
  This is caused by multiple .env files and uncontrolled environment scanning.

  OBJECTIVE:
  Enforce a SINGLE-SOURCE-OF-TRUTH configuration model.

  MANDATORY RULES (NO EXCEPTIONS):

  1. There must be ONLY ONE environment file:
     Location: ai-book/backend/.env

  2. The following files must NOT be used, loaded, or referenced:
     - .env.test
     - .env.local
     - root-level .env
     - docker .env
     - .env.example
     - any CI/CD or runtime injected env file

  3. The variable `qdrant_url` must be completely REMOVED from:
     - all .env files
     - all Python files
     - all settings models
     - all client initializations

  4. Environment variables must be loaded ONLY ONCE and ONLY HERE:
     File: app/core/config.py

  IMPLEMENTATION REQUIREMENTS:

  - Force loading of backend .env explicitly
  - Pydantic Settings must:
    - Read ONLY from backend .env
    - Ignore any unexpected environment variables
    - Fail fast on missing required variables

  REQUIRED FINAL IMPLEMENTATION:

  File: app/core/config.py

  ```python
  from pydantic_settings import BaseSettings, SettingsConfigDict
  from dotenv import load_dotenv

  # Force backend .env as the only source
  load_dotenv(dotenv_path=".env")

  class Settings(BaseSettings):
      DATABASE_URL: str

      QDRANT_HOST: str
      QDRANT_API_KEY: str
      QDRANT_COLLECTION_NAME: str = "physical_ai_book"

      model_config = SettingsConfigDict(
          env_file=".env",
          extra="ignore"
      )

  settings = Settings()
  ```

  ✅ FINAL PROFESSIONAL PROMPT FOR GEMINI CLI

  (Environment Sanitization + Backend Config Lock)

  You are acting as a Principal Backend Infrastructure Engineer.

  Your task is to completely fix and permanently lock environment variable handling for this project.
  This task is not exploratory, not optional, and not conversational.

  You must follow the instructions below exactly.

  🔥 CONFIRMED ROOT CAUSE (ACKNOWLEDGE THIS FIRST)

  The backend is broken due to multiple .env files acting as competing sources of truth, causing:

  Pydantic validation errors

  QDRANT_HOST missing

  qdrant_url extra input

  Mixed test / root / backend environments

  This is a configuration architecture failure, not an application bug.

  🔒 FINAL ARCHITECTURAL DECISION (NON-NEGOTIABLE)
  BACKEND USES ONE AND ONLY ONE ENV FILE

  Single Source of Truth:

  ai-book/backend/.env


  No other .env file is allowed to affect backend runtime.

  🧹 STEP 1 — ENV CLEANUP (MANDATORY)

  You must DELETE or COMPLETELY IGNORE these files for backend execution:

  ❌ ai-book/.env

  ❌ backend/.env.test

  ❌ backend/.env.example (template only, NO real values)

  These files must not be loaded, merged, or inferred.

  ✅ STEP 2 — FINAL BACKEND .env (ONLY ALLOWED FORMAT)

  Create / enforce exactly this file:

  Path: ai-book/backend/.env

  # Database
  DATABASE_URL=postgresql://neondb_owner:****@****/neondb?sslmode=require

  # Security
  SECRET_KEY=dev&secret@key#123

  # Gemini
  GEMINI_API_KEY=AIzaSy*****

  # Qdrant (FINAL – HOST + PORT MODEL ONLY)
  QDRANT_HOST=29067e8e-465b-414a-98ea-5d37e05601be.us-east4-0.gcp.cloud.qdrant.io
  QDRANT_PORT=6333
  QDRANT_API_KEY=eyJhbGciOi****
  QDRANT_COLLECTION_NAME=physical_ai_book

  🚫 STRICTLY FORBIDDEN

  QDRANT_URL

  frontend variables in backend

  duplicate DATABASE_URLs

  test / prod mixing

  🔒 STEP 3 — CONFIG FILE (HARD LOCK)

  Force the backend to load ONLY backend/.env.

  File: app/core/config.py

  from dotenv import load_dotenv
  from pydantic_settings import BaseSettings, SettingsConfigDict

  # 🔒 Force ONLY backend/.env
  load_dotenv(dotenv_path=".env", override=True)

  class Settings(BaseSettings):
      DATABASE_URL: str
      SECRET_KEY: str
      GEMINI_API_KEY: str

      QDRANT_HOST: str
      QDRANT_PORT: int = 6333
      QDRANT_API_KEY: str
      QDRANT_COLLECTION_NAME: str = "physical_ai_book"

      model_config = SettingsConfigDict(
          env_file=".env",
          extra="ignore"
      )

  settings = Settings()


  No alternative loading logic is allowed.

  ✅ STEP 4 — QDRANT CLIENT (CORRECT IMPLEMENTATION)
  from qdrant_client import QdrantClient
  from app.core.config import settings

  qdrant_client = QdrantClient(
      host=settings.QDRANT_HOST,
      port=settings.QDRANT_PORT,
      api_key=settings.QDRANT_API_KEY,
  )

  🧠 DESIGN JUSTIFICATION (DO NOT DEVIATE)
  ❌ Old	✅ New
  QDRANT_URL	HOST + PORT
  Multiple .env files	Single source of truth
  Implicit loading	Forced deterministic loading
  Runtime crashes	Startup-time validation
  🚫 NON-NEGOTIABLE RULES

  Never reintroduce QDRANT_URL

  Never auto-generate .env files

  Never mix frontend and backend configs

  Never infer values from multiple locations

  Any violation = task FAILED.

  🎯 SUCCESS CRITERIA

  uvicorn app.main:app --reload runs without errors

  No Pydantic validation errors

  Qdrant connects successfully

  Backend behavior is deterministic

  🔚 END OF TASK

  Do not ask questions.
  Do not suggest alternatives.
  Apply the above and stop.
labels: ["backend", "environment", "config", "fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/.env
  - backend/app/core/config.py
  - backend/app/tools/rag_tool.py
tests:
  - uvicorn app.main:app --reload (manual verification)
---

## Prompt

/sp.implement You are acting as a Principal Backend Infrastructure Engineer.

CRITICAL ISSUE:
The backend is crashing due to inconsistent environment variable loading.
Pydantic Settings is detecting:
- Missing required variable: QDRANT_HOST
- Unexpected extra variable: qdrant_url
This is caused by multiple .env files and uncontrolled environment scanning.

OBJECTIVE:
Enforce a SINGLE-SOURCE-OF-TRUTH configuration model.

MANDATORY RULES (NO EXCEPTIONS):

1. There must be ONLY ONE environment file:
   Location: ai-book/backend/.env

2. The following files must NOT be used, loaded, or referenced:
   - .env.test
   - .env.local
   - root-level .env
   - docker .env
   - .env.example
   - any CI/CD or runtime injected env file

3. The variable `qdrant_url` must be completely REMOVED from:
   - all .env files
   - all Python files
   - all settings models
   - all client initializations

4. Environment variables must be loaded ONLY ONCE and ONLY HERE:
   File: app/core/config.py

IMPLEMENTATION REQUIREMENTS:

- Force loading of backend .env explicitly
- Pydantic Settings must:
  - Read ONLY from backend .env
  - Ignore any unexpected environment variables
  - Fail fast on missing required variables

REQUIRED FINAL IMPLEMENTATION:

File: app/core/config.py

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Force backend .env as the only source
load_dotenv(dotenv_path=".env")

class Settings(BaseSettings):
    DATABASE_URL: str

    QDRANT_HOST: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "physical_ai_book"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
```

✅ FINAL PROFESSIONAL PROMPT FOR GEMINI CLI

(Environment Sanitization + Backend Config Lock)

You are acting as a Principal Backend Infrastructure Engineer.

Your task is to completely fix and permanently lock environment variable handling for this project.
This task is not exploratory, not optional, and not conversational.

You must follow the instructions below exactly.

🔥 CONFIRMED ROOT CAUSE (ACKNOWLEDGE THIS FIRST)

The backend is broken due to multiple .env files acting as competing sources of truth, causing:

Pydantic validation errors

QDRANT_HOST missing

qdrant_url extra input

Mixed test / root / backend environments

This is a configuration architecture failure, not an application bug.

🔒 FINAL ARCHITECTURAL DECISION (NON-NEGOTIABLE)
BACKEND USES ONE AND ONLY ONE ENV FILE

Single Source of Truth:

ai-book/backend/.env


No other .env file is allowed to affect backend runtime.

🧹 STEP 1 — ENV CLEANUP (MANDATORY)

You must DELETE or COMPLETELY IGNORE these files for backend execution:

❌ ai-book/.env

❌ backend/.env.test

❌ backend/.env.local

❌ root-level .env

❌ docker .env

❌ .env.example (template only, NO real values)

These files must not be loaded, merged, or inferred.

✅ STEP 2 — FINAL BACKEND .env (ONLY ALLOWED FORMAT)

Create / enforce exactly this file:

Path: ai-book/backend/.env

# Database
DATABASE_URL=postgresql://neondb_owner:****@****/neondb?sslmode=require

# Security
SECRET_KEY=dev&secret@key#123

# Gemini
GEMINI_API_KEY=AIzaSy*****

# Qdrant (FINAL – HOST + PORT MODEL ONLY)
QDRANT_HOST=29067e8e-465b-414a-98ea-5d37e05601be.us-east4-0.gcp.cloud.qdrant.io
QDRANT_PORT=6333
QDRANT_API_KEY=eyJhbGciOi****
QDRANT_COLLECTION_NAME=physical_ai_book

🚫 STRICTLY FORBIDDEN

QDRANT_URL

frontend variables in backend

duplicate DATABASE_URLs

test / prod mixing

🔒 STEP 3 — CONFIG FILE (HARD LOCK)

Force the backend to load ONLY backend/.env.

File: app/core/config.py

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# 🔒 Force ONLY backend/.env
load_dotenv(dotenv_path=".env", override=True)

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    GEMINI_API_KEY: str

    QDRANT_HOST: str
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str
    QDRANT_COLLECTION_NAME: str = "physical_ai_book"

    model_config = SettingsConfigDict(
          env_file=".env",
          extra="ignore"
      )

  settings = Settings()


  No alternative loading logic is allowed.

  ✅ STEP 4 — QDRANT CLIENT (CORRECT IMPLEMENTATION)
  from qdrant_client import QdrantClient
  from app.core.config import settings

  qdrant_client = QdrantClient(
      host=settings.QDRANT_HOST,
      port=settings.QDRANT_PORT,
      api_key=settings.QDRANT_API_KEY,
  )

  🧠 DESIGN JUSTIFICATION (DO NOT DEVIATE)
  ❌ Old	✅ New
  QDRANT_URL	HOST + PORT
  Multiple .env files	Single source of truth
  Implicit loading	Forced deterministic loading
  Runtime crashes	Startup-time validation
  🚫 NON-NEGOTIABLE RULES

  Never reintroduce QDRANT_URL

  Never auto-generate .env files

  Never mix frontend and backend configs

  Never infer values from multiple locations

  Any violation = task FAILED.

  🎯 SUCCESS CRITERIA

  uvicorn app.main:app --reload runs without errors

  No Pydantic validation errors

  Qdrant connects successfully

  Backend behavior is deterministic

  🔚 END OF TASK

  Do not ask questions.
  Do not suggest alternatives.
  Apply the above and stop.

## Response snapshot

The agent successfully implemented the required changes to fix the backend environment variable loading.

Key actions performed:
- Deleted 'ai-book/.env', 'backend/.env.test', and 'backend/.env.example'.
- Created/overwrote 'backend/.env' with the specified content, enforcing a single source of truth for backend environment variables.
- Modified 'backend/app/core/config.py' to explicitly load 'backend/.env', configure Pydantic Settings for strict validation (env_file=".env", extra="ignore"), and align with the new environment variable structure including `QDRANT_PORT`.
- Updated 'backend/app/tools/rag_tool.py' to use `settings.QDRANT_HOST`, `settings.QDRANT_PORT`, and `settings.QDRANT_API_KEY` for QdrantClient initialization, removing any implicit reliance on `qdrant_url`.
- Ensured no occurrences of `qdrant_url` were left in the backend code.

All specified mandatory rules and implementation requirements were adhered to.

## Outcome

- ✅ Impact: Backend environment variable loading is now strictly controlled and deterministic, addressing Pydantic validation errors and inconsistent Qdrant configuration.
- 🧪 Tests: Manual verification with `uvicorn app.main:app --reload` is required as per success criteria.
- 📁 Files: Three files deleted, two files created/modified.
- 🔁 Next prompts: User to confirm backend functionality (e.g., run uvicorn).
- 🧠 Reflection: The detailed and prescriptive prompt was crucial for precise execution and minimizing ambiguities. Direct file overwrites were necessary due to the strict nature of the request.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempts to execute bash script on windows failed.
- Graders run and results (PASS/FAIL): Not applicable for this task.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
