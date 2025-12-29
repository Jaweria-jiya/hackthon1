<!--
---
version_change: "0.0.0 → 1.0.0"
modified_principles:
  - "[PRINCIPLE_1_NAME]" → "1. Mission"
  - "[PRINCIPLE_2_NAME]" → "2. Core Principles"
  - "[PRINCIPLE_3_NAME]" → "3. Key Standards (Mandatory)"
  - "[PRINCIPLE_4_NAME]" → "4. Required Environment Variables (.env.example)"
  - "[PRINCIPLE_5_NAME]" → "5. Folder Structure (Strict)"
  - "[PRINCIPLE_6_NAME]" → "6. Import Rules"
added_sections:
  - "7. Build & Run Order (Safe Sequence)"
  - "8. Agents & Tools Contract"
  - "9. UX / UI Rules (Docusaurus)"
  - "10. Data Ingestion Rules"
  - "11. Deployment Rules"
  - "12. Success Criteria"
  - "13. Error Messaging Standard"
  - "14. Spec-Kit Plus Compatibility Notes"
removed_sections: []
templates_updated:
  - "✅ .specify/memory/constitution.md"
  - "⚠ .specify/templates/plan-template.md"
  - "⚠ .specify/templates/spec-template.md"
  - "⚠ .specify/templates/tasks-template.md"
todos: []
---
-->
# Physical AI & Humanoid Robotics — Docusaurus Book with Integrated RAG Chatbot Constitution

## 1. Mission

The mission of this project is to build a production-ready, deterministic, AI-native textbook that:

- Is generated using Spec-Kit Plus + Gemini CLI
- Is published with Docusaurus
- Is deployed on GitHub Pages
- Includes an integrated RAG (Retrieval-Augmented Generation) chatbot embedded directly inside the book

The chatbot stack is strictly fixed as follows:

- OpenAI Agents / ChatKit SDK
- FastAPI (backend)
- Neon Serverless Postgres
- Qdrant Cloud (free tier)

## 2. Core Principles

- **Deterministic builds:** Same spec + same command = same output. No random filenames, no timestamps inside the source tree.
- **Separation of concerns:** Frontend, Backend, Agents, Data, and Infrastructure must live in clearly separated folders.
- **Idempotence:** Every command must be repeatable. Running the same command twice must produce the same result.
- **Fail-fast errors:** Missing configuration must throw a clear, machine-readable error, for example: `ERR_MISSING_ENV: QDRANT_URL`
- **Minimal assumptions:** If cloud services are unavailable, mocks or safe fallbacks must exist.
- **Small, testable steps:** Progression must be UI → Backend → Agents → RAG → Deployment.

## 3. Key Standards (Mandatory)

### Naming Conventions

- **Folders:** kebab-case (e.g., `frontend-docusaurus`, `backend-fastapi`)
- **Python files:** `snake_case.py`
- **JavaScript / TypeScript files:** `kebab-case.js`

### Dependencies

- Frontend dependencies must be defined in `package.json`
- Backend dependencies must be defined in `requirements.txt` or `pyproject.toml`
- Versions must be pinned (no `^` for critical libraries)

### Environment Variables

- All environment variables must use `UPPER_SNAKE_CASE`
- All required variables must be listed in the root `.env.example`

### Embedding Defaults

- **Model:** `text-embedding-3-small`
- **Chunk size:** 800
- **Chunk overlap:** 50

## 4. Required Environment Variables (.env.example)

```
# Frontend / GitHub Pages
GITHUB_PAGES_REPO=
GITHUB_PAGES_BRANCH=gh-pages

# Backend
BACKEND_URL=http://localhost:8000
PORT=8000

# Authentication (BetterAuth)
BETTER_AUTH_CLIENT_ID=
BETTER_AUTH_CLIENT_SECRET=
BETTER_AUTH_BASE_URL=

# OpenAI
OPENAI_API_KEY=
OPENAI_API_BASE=

# Qdrant
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=book-chapters

# Neon Postgres
DATABASE_URL=

# RAG
EMBEDDING_MODEL=text-embedding-3-small
CHUNK_SIZE=800
CHUNK_OVERLAP=50

CI=true
```

## 5. Folder Structure (Strict)

```
/
├─ frontend-docusaurus/
├─ backend-fastapi/
├─ agents-openai/
├─ data/
│  └─ ingest/
├─ infra/
├─ spec/
│  └─ dp.specify/
├─ shared/
└─ /sp.constitution
```

### Rules

- No duplicate code across folders
- Shared logic must live only in `shared/`
- `spec/` contains prompts only (NO runtime code)

## 6. Import Rules

- Frontend may communicate with Backend only via HTTP (`/api/*`)
- Frontend must never import Python code
- Agents must run only from `agents-openai`
- Backend must call agents via HTTP
- Ingestion scripts must not be imported by runtime code

## 7. Build & Run Order (Safe Sequence)

### Environment Setup

1. Fill `.env`
2. Install backend dependencies
3. Install frontend dependencies

### Frontend

- Run `npm run start`
- Sidebar files must exist

### Backend

- `/health` endpoint must respond
- `/api/rag/query` endpoint must be available

### Agents

- Run `python -m agents_openai.runner --check-config`

### RAG Ingestion

- Run `data/ingest/ingest_chapters.py`

### Integration Test

- Query → Answer with citations

### Deployment

- **Frontend:** GitHub Pages
- **Backend:** Render or Railway

## 8. Agents & Tools Contract

### Required Agents

- `book_assistant_agent`
- `personalisation_agent_skill`
- `translation_agent_skill`

### Rules

- Vector database access is allowed only through backend endpoints
- Every response must include a `sources[]` array

## 9. UX / UI Rules (Docusaurus)

- Floating chatbot button (bottom-right)
- Personalise and Urdu buttons on every chapter
- Login required for advanced features
- Original documentation files must never be overwritten

## 10. Data Ingestion Rules

- Source of truth: `frontend-docusaurus/docs/`
- Chunked embeddings are mandatory
- Metadata per vector is required
- File hash changes must trigger selective re-ingestion

## 11. Deployment Rules

- **Frontend:** GitHub Pages
- **Backend:** Docker + Render or Railway
- Secrets must be stored only in GitHub Secrets

## 12. Success Criteria

- Book builds and deploys successfully
- Chatbot works end-to-end
- RAG answers include citations
- Authentication and personalisation work correctly

## 13. Error Messaging Standard

### Prefix-based errors:

- `ERR_MISSING_ENV`
- `ERR_INVALID_SCHEMA`
- `ERR_INGEST_FAILED`

### Exit codes:

- **0:** success
- **1:** configuration error
- **2:** runtime error
- **3:** ingestion error

## 14. Spec-Kit Plus Compatibility Notes

- Pure Markdown only
- ASCII environment variable keys only
- File path must be exactly `/sp.constitution`
- `spec/dp.specify/` must exist

## Governance

This constitution is the single source of truth for project standards and architecture. All code, infrastructure, and documentation MUST adhere to its principles. Amendments require a documented proposal, review, and an explicit migration plan for existing components.

**Version**: 1.0.0 | **Ratified**: 2025-12-13 | **Last Amended**: 2025-12-13