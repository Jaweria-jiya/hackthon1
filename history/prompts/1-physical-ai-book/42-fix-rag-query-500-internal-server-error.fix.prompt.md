--- 
id: 42
title: Fix RAG Query 500 Internal Server Error
stage: fix
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: HEAD
user: 
command: /sp.implement /sp.fix_rag_500
labels:
  - fix
  - backend
  - rag
  - qdrant
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - backend/app/api/rag/rag.py
tests_yaml:
  - N/A # Manual verification required as described
prompt_text: |-
  ---
  description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
  ---

  ## User Input

  ```text
  $ARGUMENTS
  ```

  You **MUST** consider the user input before proceeding (if not empty).

  ## Outline

  1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

  2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
     - Scan all checklist files in the checklists/ directory
     - For each checklist, count:
       - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
       - Completed items: Lines matching `- [X]` or `- [x]`
       - Incomplete items: Lines matching `- [ ]`
     - Create a status table:

       ```text
       | Checklist | Total | Completed | Incomplete | Status | 
       |-----------|-------|-----------|------------|--------|
       | ux.md     | 12    | 12        | 0          | ✓ PASS |
       | test.md   | 8     | 5         | 3          | ✗ FAIL |
       | security.md | 6   | 6         | 0          | ✓ PASS |
       ```

     - Calculate overall status:
       - **PASS**: All checklists have 0 incomplete items
       - **FAIL**: One or more checklists have incomplete items

     - **If any checklist is incomplete**:
       - Display the table with incomplete item counts
       - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
       - Wait for user response before continuing
       - If user says "no" or "wait" or "stop", halt execution
       - If user says "yes" or "proceed" or "continue", proceed to step 3

  3. Load and analyze the implementation context:
     - **REQUIRED**: Read tasks.md for the complete task list and execution plan
     - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
     - **IF EXISTS**: Read data-model.md for entities and relationships
     - **IF EXISTS**: Read contracts/ for API specifications and test requirements
     - **IF EXISTS**: Read research.md for technical decisions and constraints
     - **IF EXISTS**: Read quickstart.md for integration scenarios

  4. **Project Setup Verification**:
     - **REQUIRED**: Create/verify ignore files based on actual project setup:

     **Detection & Creation Logic**:
     - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

       ```sh
       git rev-parse --git-dir 2>/dev/null
       ```

     - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
     - Check if .eslintrc*or eslint.config.* exists → create/verify .eslintignore
     - Check if .prettierrc* exists → create/verify .prettierignore
     - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
     - Check if terraform files (*.tf) exist → create/verify .terraformignore
     - Check if .helmignore needed (helm charts present) → create/verify .helmignore

  5. Parse tasks.md structure and extract:
     - **Task phases**: Setup, Tests, Core, Integration, Polish
     - **Task dependencies**: Sequential vs parallel execution rules
     - **Task details**: ID, description, file paths, parallel markers [P]
     - **Execution flow**: Order and dependency requirements

  6. Execute implementation following the task plan:
     - **Phase-by-phase execution**: Complete each phase before moving to the next
     - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together
     - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
     - **File-based coordination**: Tasks affecting the same files must run sequentially
     - **Validation checkpoints**: Verify each phase completion before proceeding

  7. Implementation execution rules:
     - **Setup first**: Initialize project structure, dependencies, configuration
     - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
     - **Core development**: Implement models, services, CLI commands, endpoints
     - **Integration work**: Database connections, middleware, logging, external services
     - **Polish and validation**: Unit tests, performance optimization, documentation

  8. Progress tracking and error handling:
     - Report progress after each completed task
     - Halt execution if any non-parallel task fails
     - For parallel tasks [P], continue with successful tasks, report failed ones
     - Provide clear error messages with context for debugging
     - Suggest next steps if implementation cannot proceed
     - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

  9. Completion validation:
     - Verify all required tasks are completed
     - Check that implemented features match the original specification
     - Validate that tests pass and coverage meets requirements
     - Confirm the implementation follows the technical plan
     - Report final status with summary of completed work

  Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/sp.tasks` first to regenerate the task list.

  ---

  As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

  1) Determine Stage
     - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

  2) Generate Title and Determine Routing:
     - Generate Title: 3–7 words (slug for filename)
     - Route is automatically determined by stage: 
       - `constitution` → `history/prompts/constitution/`
       - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
       - `general` → `history/prompts/general/`

  3) Create and Fill PHR (Shell first; fallback agent‑native)
     - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
     - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
     - If the script fails:
       - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
       - Allocate an ID; compute the output path based on stage from step 2; write the file
       - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

  4) Validate + report
     - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
     - On failure: warn, don't block. Skip only for `/sp.phr`.
response_text: |-
  I have reviewed `backend/app/api/rag/rag.py`.

  The code structure looks generally correct for a RAG pipeline. It performs:
  1.  Environment variable checks.
  2.  Initialization of `OpenAIEmbeddings` and `QdrantClient`.
  3.  Embedding generation for the query.
  4.  Qdrant search.
  5.  Processing and returning results.

  The most likely causes for a `500 Internal Server Error` given this code and the problem description are:

  *   **Environment Variables Missing/Incorrect:** The `get_rag_dependencies` function explicitly checks for `OPENAI_API_KEY` and `QDRANT_HOST`. If `QDRANT_API_KEY` is missing or incorrect, it won't raise an `HTTPException` in `get_rag_dependencies` but will likely cause a failure when `QdrantClient` tries to connect or authenticate.
  *   **Qdrant Connection Issues:** Even if `QDRANT_HOST` and `QDRANT_API_KEY` are present, Qdrant might not be accessible or the collection might not exist.
  *   **OpenAI Embeddings Issues:** Problems with `OPENAI_API_KEY` (e.g., invalid key, rate limits) could cause `embeddings_model.embed_query` to fail.
  *   **Collection Name Issue:** If `QDRANT_COLLECTION_NAME` is incorrect or the collection doesn't exist in Qdrant.
  *   **Payload Structure Mismatch:** If the data stored in Qdrant (the `payload` of each `hit`) does not contain "content", "source", or "chunk_id" as expected, the `payload.get(...)` calls might lead to unexpected behavior or `None` values that cause downstream issues, though the `.get()` method handles missing keys gracefully.

  The current `except Exception as e: raise HTTPException(...)` block at the end of `rag_query` will catch any unhandled exception and return a 500 with the exception message. This is good for debugging but not for production.

  **Root Cause Analysis based on provided information:**

  The user states:
  - `/api/rag/query` returns 500 Internal Server Error
  - Auth is working (login 200 OK)
  - Token present

  This suggests the issue is specific to the RAG component and not authentication or general API connectivity.

  The critical issue that stands out is the lack of a check for `QDRANT_API_KEY` in `get_rag_dependencies`. If this key is missing, `QdrantClient` initialization or subsequent operations would fail, leading to a 500 error.

  Also, the `OpenAIEmbeddings` class likely uses `OPENAI_API_KEY` directly from the environment during initialization if not passed. Passing it explicitly is good practice.

  **Proposed Fixes:**

  1.  **Add `QDRANT_API_KEY` environment variable check:** Explicitly check for `QDRANT_API_KEY` in `get_rag_dependencies` to provide a clear error message early.
  2.  **Ensure `OpenAIEmbeddings` is correctly initialized:** Confirm `openai_api_key` is passed to `OpenAIEmbeddings`. (It already is, which is good).
  3.  **Refine error handling:** While the generic `except Exception` catches everything, for production, it's better to catch specific expected exceptions (e.g., from Qdrant or OpenAI) and return more specific `HTTPException` details. However, for a quick fix, ensuring all environment variables are checked is paramount.

  Let's start with adding the `QDRANT_API_KEY` check.

  **File + line number:** `backend/app/api/rag/rag.py`, around line 28 (where `QDRANT_HOST` is checked).
file_path: history/prompts/1-physical-ai-book/42-fix-rag-query-500-internal-server-error.fix.prompt.md
