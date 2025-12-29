---
id: 39
title: Remove Broken Auth References and Fix Build
stage: fix
date: 2025-12-22
surface: agent
model: Gemini
feature: 001-physical-ai-book
branch: 1-physical-ai-book
user: user
command: /sp.implement
labels: ["bugfix", "build-error", "cleanup", "authentication"]
links:
  spec: specs/001-physical-ai-book/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/src/theme/Layout/index.tsx
 - frontend-docusaurus/website/src/components/progress/Progress.tsx
 - frontend-docusaurus/website/src/components/notes/Notes.tsx
 - frontend-docusaurus/website/src/components/auth/Login.tsx
 - frontend-docusaurus/website/src/components/auth/Profile.tsx
 - frontend-docusaurus/website/src/components/auth/Signup.tsx
 - frontend-docusaurus/website/src/pages/profile.tsx
 - frontend-docusaurus/website/src/theme/Navbar/MobileSidebar/Layout/index.tsx
tests:
 - npm run typecheck
 - npm run build
---

## Prompt

/sp.implement You are working in an existing frontend codebase (Docusaurus + React).

TASK TYPE: FRONTEND ERROR FIX (CLEANUP ONLY)
GOAL: REMOVE BROKEN AUTH REFERENCES WITHOUT ADDING NEW FEATURES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROBLEM CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The frontend build is failing with errors like:

"Module not found: Can't resolve '@site/src/contexts/AuthContext'"

The AuthContext file has already been deleted intentionally.
Now all leftover imports and usages must be cleaned up properly.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIRED ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ REMOVE AuthContext IMPORTS
- Search the entire frontend codebase for:
  '@site/src/contexts/AuthContext'
- Remove ALL imports of AuthContext from every file.

Affected folders include (but not limited to):
- src/components/auth
- src/components/notes
- src/components/progress
- src/theme/Layout

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣ REMOVE AUTH-DEPENDENT LOGIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For any component that was using AuthContext:
- Remove useContext(AuthContext)
- Remove auth-related variables (user, isAuthenticated, etc.)
- Remove conditional rendering based on auth state
- Simplify the component so it works without authentication

⚠️ Do NOT replace AuthContext with another auth system.
⚠️ Do NOT introduce mock auth.
⚠️ Do NOT add new logic.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3️⃣ DELETE UNUSED AUTH COMPONENTS (IF ANY)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If any components exist that ONLY served authentication purposes:
- Delete those components completely.
- Remove their imports from other files.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4️⃣ CRITICAL RULES (VERY IMPORTANT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- DO NOT recreate AuthContext.
- DO NOT add new auth files.
- DO NOT refactor unrelated UI.
- DO NOT leave commented-out code.
- ONLY REMOVE broken references and simplify code.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5️⃣ FINAL VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After cleanup:
- The frontend MUST compile successfully.
- There must be ZERO references to:
  - AuthContext
  - useAuth
  - authentication state
- No new errors should be introduced.

Before finishing, run a full frontend build and ensure it passes without errors.

## Response snapshot

I have successfully removed all broken authentication references from the frontend codebase.

**Summary of Cleanup:**

1.  **AuthContext References Removed:** I systematically searched for and removed all imports and usages of `AuthContext` and the `useAuth` hook from all affected components (`Layout`, `Progress`, `Notes`, and the `auth` components).
2.  **Auth-Dependent Logic Removed:** Components that relied on authentication state (`Progress`, `Notes`) have been simplified to display a generic "feature unavailable" message, removing their dependency on a user object.
3.  **Unused Components Deleted:** The auth-only components (`Login.tsx`, `Profile.tsx`, `Signup.tsx`) and the related page (`profile.tsx`) were deleted.
4.  **Build Verification:** To fix the build, I also had to resolve an unrelated, pre-existing TypeScript error in a Docusaurus theme file (`MobileSidebar/Layout/index.tsx`). After all cleanup, I ran `npm run typecheck` and `npm run build`, and both commands completed successfully, confirming the absence of any build or type errors.

The frontend is now in a clean, compilable state with all specified authentication references removed.

## Outcome

- ✅ Impact: Fixed the frontend build, which was failing due to broken references to a deleted `AuthContext`. All related dead code, components, and pages have been removed, resulting in a clean, compilable state.
- 🧪 Tests: Successfully ran `npm run typecheck` and `npm run build` after the cleanup to confirm the absence of any build-time or type-checking errors.
- 📁 Files: Removed `AuthContext` imports and usage from multiple files, deleted unused auth components and pages, and fixed an unrelated but build-blocking type error in a Docusaurus theme file.
- 🔁 Next prompts: The frontend can now be run or deployed, as the build is successful.
- 🧠 Reflection: The task was primarily a systematic cleanup of broken imports. It also required fixing an unexpected, unrelated type error in a theme file to unblock the build and fully verify the cleanup.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment: none
