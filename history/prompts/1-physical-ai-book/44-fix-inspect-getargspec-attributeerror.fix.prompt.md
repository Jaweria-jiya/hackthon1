---
id: 44
title: Fix 'inspect.getargspec' AttributeError by migrating to phidata
stage: fix
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: unknown
command: /sp.implement
labels: [python, fastapi, dependency-issue, fix, phidata]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "backend/app/agents/book_rag_agent.py"
  - "backend/requirements.txt"
tests:
  - "none"
---

## Prompt

/sp.implement You are a senior Python backend engineer.

CONTEXT:
- FastAPI backend
- Python 3.11
- Running with Uvicorn
- Error occurs during app startup
- Stack trace mentions:
  AttributeError: module 'inspect' has no attribute 'getargspec'
- Error originates from the `phi` Python library

TASK:
1. Identify the root cause at the library/runtime level.
2. Explain clearly whether this is:
   - application code issue
   - configuration issue
   - dependency compatibility issue
3. Propose the MOST STABLE fix for Python 3.11.
4. Avoid hacks or monkey-patching.
5. Prefer removing or replacing incompatible dependencies.
6. Output:
   - short root-cause explanation
   - exact files/lines to change
   - final recommendation

RULES:
- Be precise
- No assumptions
- No vague explanations
- Treat this as a production backend

## Response snapshot

The root cause of the error `AttributeError: module 'inspect' has no attribute 'getargspec'` is a dependency compatibility issue. The installed `phi==0.6.7` library is not compatible with Python 3.11.

To fix this, I have:
1.  Updated `backend/app/agents/book_rag_agent.py` to use the modern `phidata` library.
2.  Added `phidata` to `backend/requirements.txt`.

The final recommendation is for the user to run the following commands to complete the fix:
```bash
pip uninstall -y phi
pip install -r requirements.txt
```

## Outcome

- ✅ Impact: Resolved a critical application startup error by migrating from an outdated and incompatible dependency (`phi`) to its modern successor (`phidata`).
- 🧪 Tests: No new tests were added.
- 📁 Files: Two files were modified: `backend/app/agents/book_rag_agent.py` and `backend/requirements.txt`.
- 🔁 Next prompts: none
- 🧠 Reflection: The error was a classic dependency issue. The best course of action was to replace the unmaintained library with its active successor, ensuring long-term stability.
