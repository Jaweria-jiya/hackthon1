---
id: 115
title: Move Translate Button to Breadcrumb Area
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement
labels: ["refactor", "ui", "button-placement", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/src/theme/DocItem/Layout/index.tsx (modified)
 - frontend-docusaurus/website/src/theme/DocItem/Layout/styles.module.css (modified)
tests:
 - No tests were run or added.
---

## Prompt

/sp.implement You are an expert Docusaurus developer specializing in swizzling theme components, layout customization, and precise placement of custom UI elements.

Project: A Docusaurus book/site titled "Physical AI & Humanoid Robotics" using the classic theme.

Current setup:
- There is a custom "Translate to Urdu" button visible on every documentation page.
- It currently appears somewhere in the page content area (likely in the main content or sidebar).

Desired change:
- Move the "Translate to Urdu" button to the breadcrumb/navigation path area on every page.
- Specifically, place it on the same horizontal line where the breadcrumb trail is displayed, right after the last breadcrumb item.
- Example of desired placement:
  Home → Module 2: Digital Twin (Gazebo & Unity) → Unity for Human-Robot Interaction (HRI)   [Translate to Urdu button here]

Requirements:
- The button should appear on the same line as the breadcrumbs, aligned horizontally (preferably to the right of the last breadcrumb item).
- Keep the existing breadcrumb structure and home icon fully intact — do not modify or hide any part of it.
- The button should appear consistently on every docs/book page.
- Maintain existing functionality (including any auth redirect logic).
- Ensure responsive design: on mobile, it should either stay on the same line (if space allows) or move gracefully below without breaking layout.

Implementation:
1. Identify where the "Translate to Urdu" button is currently rendered (likely a custom component in src/components/ or injected via swizzled DocItem).
2. The breadcrumb area is typically rendered in the Navbar or in the theme's DocItem/Layout or Breadcrumbs component.
3. Best approach: Swizzle the Breadcrumbs component (npx docusaurus swizzle @docusaurus/theme-classic Breadcrumbs -- --eject) or the DocItem/Layout.
4. In the swizzled Breadcrumbs.js (or equivalent), insert the TranslateToUrdu component right after the last breadcrumb item, with appropriate styling (inline-flex, margin-left, etc.).
5. Provide exact code changes with clear placement.

Provide:
- Step-by-step instructions (including swizzle command if needed).
- Exact file to modify (e.g., src/theme/Breadcrumbs/index.js or src/theme/DocItem/Layout.js).
- Full updated code snippet showing where to insert the button.
- Any required CSS for alignment (e.g., in custom.css) to make it sit perfectly on the same line.
- Ensure it only appears on doc pages (not on homepage or blog if not needed).

Output only the solution in a clean, structured format with code blocks. No extra commentary.l

## Response snapshot

Successfully moved the 'Translate to Urdu' button to the breadcrumb area on docs pages, aligned horizontally with breadcrumbs, and maintaining functionality.

## Outcome

- ✅ Impact: Improved UI layout on docs pages by repositioning the 'Translate to Urdu' button to the breadcrumb area, enhancing visual consistency and user experience.
- 🧪 Tests: Visual inspection and functional testing required; no automated tests were available for this UI refactoring task.
- 📁 Files: Modified `DocItem/Layout/index.tsx` and `DocItem/Layout/styles.module.css`.
- 🔁 Next prompts: Awaiting further instructions on code implementation of RAG answering rules or other tasks.
- 🧠 Reflection: The task involved precisely repositioning a custom button within a swizzled Docusaurus theme component (`DocItem/Layout`). This required wrapping the button and breadcrumbs in a new flex container and applying appropriate CSS for horizontal alignment, ensuring responsiveness and functional integrity.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
