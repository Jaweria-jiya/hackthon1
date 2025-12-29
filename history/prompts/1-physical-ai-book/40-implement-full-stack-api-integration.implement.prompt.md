---
id: 40
title: Implement Full-Stack API Integration
stage: implement
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: unknown
command: /sp.implement P4-T4: API Integration
labels: [api-integration, full-stack, backend, frontend]
links:
  spec: "specs/001-physical-ai-book/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".env.template"
  - "backend/app/core/config.py"
  - "backend/app/main.py"
  - "backend/app/api/rag/chat.py"
  - "frontend-docusaurus/website/docusaurus.config.ts"
  - "frontend-docusaurus/website/src/services/api.ts"
  - "frontend-docusaurus/website/src/theme/Root.tsx"
  - "IMPLEMENTATION_INSTRUCTIONS.md"
tests:
  - "none"
---

## Prompt

/sp.implement P4‑T4: API Integration

Frontend ↔ Backend

Frontend ↔ Chatbot You are a senior software engineer with expertise in full-stack development, API integrations, and error-free production-ready code.

Project Context:
- We have a FastAPI backend (Python) and a frontend (React or Docusaurus-based).
- There is an integrated chatbot (using phi/OpenAI agents).
- We want perfect API communication:
  1. Frontend ↔ Backend
  2. Frontend ↔ Chatbot
- Environment variables must be defined in a single .env file.
- All environment variables must be imported properly in Python and frontend code.
- No import errors, no missing code, no typos, no syntax issues.
- Code must follow professional conventions (clear structure, proper imports, strict error handling).

Task:
1. Implement the API integration between frontend and backend, and frontend and chatbot.
2. Ensure backend exposes all endpoints correctly and consumes env variables from `.env`.
3. Ensure frontend calls backend APIs and chatbot endpoints correctly.
4. Use proper async/await patterns where required.
5. Ensure Python code is compatible with the correct Python version and all dependencies are installed.
6. Create a fully working `.env` template and load it correctly in both frontend and backend.
7. Generate professional, clean, production-ready folder structure and code for all files.
8. Provide instructions to run frontend and backend without any errors.

Requirements:
- Strictly follow best practices for Python (FastAPI), JavaScript/TypeScript (frontend), and env variable usage.
- No deprecated or incompatible methods.
- Fully working, copy-paste ready code.

Output:
- Step-by-step professional instructions.
- All code files and folder structure.
- Correct `.env` template.
- Commands to run backend, frontend, and chatbot successfully.

Respond **as if you are a professional software engineer delivering a production-ready system**, not a guide or explanation.

## Response snapshot

I have successfully implemented the API integration between the frontend, backend, and chatbot. I have provided a detailed instruction file named `IMPLEMENTATION_INSTRUCTIONS.md` with all the steps to set up and run the project.

## Outcome

- ✅ Impact: The API integration is complete, enabling communication between the frontend and backend services.
- 🧪 Tests: No new tests were added.
- 📁 Files: 8 files were created or modified to implement the API integration.
- 🔁 Next prompts: none
- 🧠 Reflection: The task was complex but well-defined. The existing project structure was helpful in understanding the requirements.
