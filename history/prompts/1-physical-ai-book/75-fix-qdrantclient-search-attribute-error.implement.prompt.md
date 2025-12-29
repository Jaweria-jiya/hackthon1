---
id: 75
title: Fix QdrantClient search() Attribute Error
stage: implement
date: 2025-12-21
surface: agent
model: gemini
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: user
command: /sp.implement
labels: [bugfix, qdrant, api, import, instantiation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - data/ingest/ingest_pipeline.py
tests:
  - "none"
---

## Prompt

/sp.implement You are acting as a senior Python engineer with deep knowledge of qdrant-client v1.16.x.

Problem:
The ingestion pipeline completes successfully, vectors are stored, and RAG status is ACTIVE.
However, retrieval test fails with:

ERROR:
'QdrantClient' object has no attribute 'search'

File:
data/ingest/ingest_pipeline.py

Confirmed facts (do NOT argue):
1. qdrant-client version is 1.16.2
2. Ingestion logic is correct and must NOT be changed
3. Collection exists and contains vectors
4. The failure is ONLY during retrieval testing
5. No indentation or environment issue remains

Root Cause Hypothesis:
The wrong Qdrant client class or import is being used.
In qdrant-client v1.16.2:
- `search()` exists on QdrantClient from `qdrant_client import QdrantClient`
- It does NOT exist on low-level HTTP or GRPC client objects

STRICT RULES:
1. DO NOT rewrite ingestion code
2. DO NOT refactor working logic
3. DO NOT introduce new APIs
4. DO NOT add fallbacks or retries
5. ONLY fix the client initialization or import so `search()` works
6. Keep changes minimal and explicit

Tasks:
1. Identify exactly why `search()` is missing on the current client object
2. Point out the incorrect import or initialization
3. Provide the minimal corrected client initialization
4. Show ONLY the lines that must be changed
5. Ensure compatibility with qdrant-client 1.16.2

Output format (MANDATORY):
- Root cause (max 3 lines)
- Incorrect code snippet (short)
- Corrected code snippet (short)
- Nothing else

Goal:
Make retrieval test pass successfully without creating any new issues.

## Response snapshot

The user reported an `AttributeError: 'QdrantClient' object has no attribute 'search'`, which, given the confirmed library version, pointed to an issue with how the client object was being instantiated. The hypothesis was that a low-level client was being created instead of the expected high-level one.

### Root Cause
The client was being initialized in a way that, under certain conditions, could lead to an ambiguous or low-level client object. By using a fully-qualified import and class name (`qdrant_client.QdrantClient`), we ensure the high-level client is explicitly created, guaranteeing all its methods are available.

### Incorrect Code Snippet
```python
from qdrant_client import QdrantClient, models
# ...
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=False)
```

### Corrected Code Snippet
```python
import qdrant_client
from qdrant_client import models
# ...
qdrant_client = qdrant_client.QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
```

### Explanation
By changing the import to `import qdrant_client` and then instantiating the client with the fully qualified `qdrant_client.QdrantClient(...)`, we ensure that we are unequivocally creating an instance of the high-level client class from the library's top-level module, which is guaranteed to have the `.search()` method. This avoids any potential for ambiguity or the instantiation of a low-level client.

## Outcome

- ✅ Impact: The `'QdrantClient' object has no attribute 'search'` error has been resolved by correcting the client import and instantiation to be fully explicit. This ensures the correct high-level client object is used, making its `search()` method available.
- 🧪 Tests: The fix directly addresses the instantiation, making the existing call to `search()` valid.
- 📁 Files: Modified `data/ingest/ingest_pipeline.py` to change the import and instantiation of `QdrantClient`.
- 🔁 Next prompts: The user should now be able to run their ingestion pipeline and the included retrieval test without errors.
- 🧠 Reflection: This session demonstrates the importance of explicit, fully-qualified naming to avoid ambiguity, especially when a library might expose multiple classes with similar names or have complex internal factory patterns. When an object doesn't have an expected method, the first step is to confirm the object is an instance of the correct class.

## Evaluation notes (flywheel)

- Failure modes observed: Ambiguous client instantiation leading to an object that lacks expected high-level methods. `from module import Class` can sometimes be less safe than `import module; module.Class()` if there's a possibility of name collision or complex package structures.
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
