---
id: 114
title: Redirect Unauthenticated Translate User to Signup
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement
labels: ["refactor", "auth", "ui", "translation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/src/theme/DocItem/Layout/index.tsx (modified)
tests:
 - No tests were run or added.
---

## Prompt

/sp.implement You are an expert Docusaurus developer with experience in custom plugins, authentication integration, and event handling for UI components like buttons.

Project: A Docusaurus book/site titled "Physical AI & Humanoid Robotics" with authentication (Sign In/Sign Up) and a "Translate to Urdu" button on every page.

Current behavior:
- The "Translate to Urdu" button is visible on every page (perfect, do not change visibility).
- When clicked:
  - If user is logged in, it performs the translation (keep this functionality intact).
  - If user is NOT logged in (no account), it currently shows an alert (e.g., "Please log in to translate").

Desired change:
- Modify ONLY the non-logged-in case: Instead of showing an alert, directly redirect the user to the /signup page.
- This informs the user they need an account to translate, without disrupting the flow.
- Do NOT change anything else: Keep translation working for logged-in users, button visibility, and all other site features.

Implementation assumptions:
- Authentication is likely handled via a context/provider (e.g., AuthContext) checking isLoggedIn or similar.
- The button is probably a custom component (e.g., in src/components/TranslateButton.js) or added via a plugin/swizzled DocItem.
- The click handler is in the button's onClick event, which checks auth and alerts if not authenticated.

Solution steps:
1. Locate the "Translate to Urdu" button code (likely in src/pages or a swizzled theme component like DocItem/Content or a custom plugin).
2. In the button's onClick handler:
   - Check if user is authenticated (e.g., if (!isLoggedIn)).
   - If not, replace the alert() with a redirect: window.location.href = '/signup'; or use React Router's navigate('/signup').
3. If using React hooks/context, provide example code with useContext or similar.
4. Ensure redirect preserves the current page URL (e.g., pass as query param ?returnTo=currentPath) if needed for post-signup redirect back to translation.

Provide:
- Exact file(s) to modify (e.g., src/components/TranslateButton.js).
- Full updated code snippet for the onClick handler.
- If it's a plugin, suggest plugin config changes.
- Step-by-step instructions to apply the fix.
- Ensure the change is clean, professional, and doesn't break existing functionality.

Output only the solution in a structured format with code blocks. No unrelated content.

## Response snapshot

Successfully modified the 'Translate to Urdu' button's `onClick` handler to redirect unauthenticated users directly to the `/signup` page, removing the intermediate alert.

## Outcome

- ✅ Impact: Improved user experience for unauthenticated translation attempts by replacing an alert with a direct redirect to the signup page.
- 🧪 Tests: Visual inspection and functional testing of the button's non-logged-in behavior are required; no automated tests were available for this UI logic modification.
- 📁 Files: Modified `frontend-docusaurus/website/src/theme/DocItem/Layout/index.tsx`.
- 🔁 Next prompts: Awaiting further instructions on code implementation of RAG answering rules or other tasks.
- 🧠 Reflection: The task involved precisely locating and modifying the authentication check within a swizzled Docusaurus component (`DocItem/Layout`). The existing code already contained the redirect, so the fix was simply removing the `alert()` call, streamlining the user flow as requested.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
