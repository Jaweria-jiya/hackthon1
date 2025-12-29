---
id: 40
title: Refactor Authentication Flow Implementation
stage: implement
date: 2025-12-16
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: HEAD
user: 
command: /sp.implement P5T1
labels:
  - implement
  - refactor
  - auth
  - docusaurus
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/001-physical-ai-book/tasks.md
  - frontend-docusaurus/website/src/contexts/AuthContext.tsx
  - frontend-docusaurus/website/src/components/ProtectedRoute.tsx (removed)
  - frontend-docusaurus/website/docs/intro.md (restored from .mdx)
  - frontend-docusaurus/website/docs/intro.mdx (removed)
  - frontend-docusaurus/website/src/theme/DocRoot/Layout/index.tsx
  - frontend-docusaurus/website/src/theme/Navbar/Layout/index.tsx
tests_yaml: []
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
response_text: "All implementation tasks (T001 to T008) from Phase 1, 2, and 3 have been completed. The remaining tasks (T009, T010, T011) are for verification and end-to-end testing.

**Summary of Changes:**

*   **`frontend-docusaurus/website/src/contexts/AuthContext.tsx`**:
    *   Introduced a `loading` state to manage the asynchronous nature of checking authentication status from `localStorage` on initial load.
    *   The `AuthContextType` and `AuthContext.Provider` now expose this `loading` state.
*   **`frontend-docusaurus/website/src/components/ProtectedRoute.tsx`**:
    *   This file was removed as it was identified as an anti-pattern for Docusaurus route protection.
*   **`frontend-docusaurus/website/docs/intro.md` and `intro.mdx`**:
    *   The `intro.mdx` file was reverted to `intro.md`, and the `<ProtectedRoute>` wrapper was removed, as per Docusaurus best practices for route protection.
*   **`frontend-docusaurus/website/src/theme/DocRoot/Layout/index.tsx`**:
    *   The `DocRoot` component was swizzled to implement route protection at the layout level.
    *   It now uses `useAuth()` to check `user` and `loading` states. If `loading` is true, it displays a "Loading..." message. If `loading` is false and no `user` is present, it redirects to the `/login` page.
*   **`frontend-docusaurus/website/src/theme/Navbar/Layout/index.tsx`**:
    *   Modified to consume the `loading` state from `useAuth()`. 
    *   It now renders a placeholder (e.g., "...") while the authentication state is being determined, preventing UI flickering.

**Explanation of Why Previous Approach Failed (as requested in task context):**

The previous approach suffered from several critical issues:

1.  **Login Loop due to `ProtectedRoute` and `user` state:** The `ProtectedRoute` component was relying solely on the in-memory `user` state from `AuthContext`. When a page refreshed, this `user` state was momentarily null before `localStorage` could rehydrate it, causing a rapid redirect to `/login` even for authenticated users, leading to a login loop. This was exacerbated by `ProtectedRoute` being applied directly to MDX files, which is not an idiomatic way to handle route protection in Docusaurus.
2.  **Auth State Not Stabilized before Redirect:** There was no explicit `loading` state to indicate when the authentication check was in progress. This meant that components (like `ProtectedRoute` or the Navbar) might attempt to render based on an incomplete or outdated authentication status, leading to incorrect redirects or UI flashes.
3.  **Docs Protected via MDX Wrapping (Anti-Pattern):** Wrapping content directly within MDX files using a `ProtectedRoute` is brittle and difficult to maintain. It couples the content directly to authentication logic, making it less modular and prone to issues with Docusaurus's build process or routing.
4.  **Navbar Dependence on Async User State Only:** Similar to the `ProtectedRoute`, the Navbar was rendering based on the `user` state without considering an intermediate `loading` state. This could cause a brief display of "Login/Sign Up" links even when a user was technically authenticated but their state hadn't been fully restored from `localStorage`.

The refactored approach addresses these by:

*   Establishing `access_token` in `localStorage` as the primary source of truth for persistent authentication.
*   Introducing a `loading` state in `AuthContext` to stabilize authentication status before any rendering or redirection logic is applied.
*   Implementing route protection at the Docusaurus layout level (`DocRoot/Layout`) using swizzling, which is a standard and robust method for customizing Docusaurus themes. This decouples authentication logic from content files.
*   Ensuring UI components (Navbar, DocRootLayout) gracefully handle the `loading` state, preventing flickering and incorrect renders.

**Verification Steps (Tasks T009, T010, T011):**

To verify these fixes, you should:

1.  **Start the frontend and backend applications.**
    *   Backend: Navigate to `backend/` and run `uvicorn app.main:app --reload`.
    *   Frontend: Navigate to `frontend-docusaurus/website/` and run `npm start`.
2.  **Open your browser** to the Docusaurus frontend (usually `http://localhost:3000`).
3.  **Verify Navbar without login:**
    *   You should see "Login" and "Sign Up" links in the navbar (after a brief "..." loading state).
    *   Attempt to navigate to any `/docs/*` route (e.g., `/docs/intro`). You should be redirected to the `/login` page.
4.  **Register a new user:**
    *   Click "Sign Up" in the navbar.
    *   Fill in a new email and password, then click "Sign Up".
    *   You should be redirected to the `/login` page after successful registration.
5.  **Log in with the new user:**
    *   Enter the registered email and password.
    *   Click "Login".
    *   You should be redirected to `/docs/intro`.
6.  **Verify Navbar after login:**
    *   You should now see your email, a "Profile" link, and a "Logout" button in the navbar.
    *   Verify that you can access `/docs/intro` and other doc pages.
7.  **Verify Token Persistence & No Redirect on Refresh (T010):**
    *   Refresh the page (`/docs/intro`).
    *   You should still be logged in (your email in the navbar should persist), demonstrating that the authentication state is restored from `localStorage` without redirecting to `/login`.
8.  **Verify Logout:**
    *   Click the "Logout" button in the navbar.
    *   You should be redirected to the homepage or login page, and the navbar should revert to showing "Login" and "Sign Up" links.
    *   Attempt to access any `/docs/*` route again; you should be redirected to `/login`.
9.  **Conduct end-to-end testing of the authentication flow (T011):**
    *   Test all combinations of login, logout, page refreshes, and direct navigation to protected/unprotected routes to ensure no redirect loops or unexpected behavior."
file_path: history/prompts/1-physical-ai-book/40-refactor-authentication-flow-implementation.implement.prompt.md
