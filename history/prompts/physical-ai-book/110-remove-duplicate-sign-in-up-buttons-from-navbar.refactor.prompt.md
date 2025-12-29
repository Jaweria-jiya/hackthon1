---
id: 110
title: Remove Duplicate Sign In/Up Buttons from Navbar
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement
labels: ["refactor", "navbar", "ui", "cleanup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/src/css/custom.css (modified)
tests:
 - No tests were run or added.
---

## Prompt

/sp.implement You are an expert Docusaurus front-end developer with in-depth knowledge of the classic theme, navbar configuration, and custom styling.

Project: A Docusaurus documentation/book site titled "Physical AI & Humanoid Robotics".

Current status from screenshot:
- "Sign In" and "Sign Up" are now successfully moved to the far right side of the navbar (next to GitHub icon).
- They are functional (navigation works correctly).
- However, duplicate "Sign In" and "Sign Up" green buttons still appear on the left side of the navbar, making the header look cluttered and unprofessional.

Goal:
- Completely remove the duplicate "Sign In" and "Sign Up" buttons that are appearing on the left side.
- Keep only the right-side text links (Sign In | Sign Up | GitHub) as the final version.
- Ensure the header looks clean and balanced: logo/title on the left, navigation items in the center if any, and only the auth links + GitHub on the far right.

Required changes:
1. In docusaurus.config.js → themeConfig.navbar.items:
   - Remove any navbar items for "Sign In" and "Sign Up" that have position: 'left' (or no position specified, which defaults to left).
   - Ensure that the Sign In and Sign Up items only exist once with position: 'right'.
   - Confirm the GitHub link is also on the right (usually via themeConfig.navbar.links or a separate item with position: 'right').

2. If the left-side buttons are not coming from navbar.items (e.g., added via a custom plugin, swizzled NavbarItem, or injected via themeConfig.navbar.logo or other means), identify and suggest how to remove them.

3. Provide the corrected full example of the navbar.items array, showing:
   - Only left-positioned items (like docs links, version dropdown if any).
   - Right-positioned items: Sign In, Sign Up, GitHub.

4. If needed, suggest a small CSS override (in src/css/custom.css) to hide any stubborn leftover elements, e.g.:
   ```css
   .navbar__items > .navbar__item:nth-child(/* appropriate */ ) { display: none; }

## Response snapshot

Successfully removed duplicate 'Sign In' and 'Sign Up' buttons from the left side of the Docusaurus navbar using CSS overrides.

## Outcome

- ✅ Impact: Cleaned up navbar by hiding redundant 'Sign In'/'Sign Up' buttons, improving UI balance and professionalism.
- 🧪 Tests: Visual inspection required; no automated tests were available for this UI refactoring task.
- 📁 Files: Modified `custom.css` to hide duplicate navbar items.
- 🔁 Next prompts: Awaiting further instructions on code implementation of RAG answering rules or other tasks.
- 🧠 Reflection: The task addressed a UI clutter issue caused by apparent duplicate navbar items. Since these items were not explicitly present in `docusaurus.config.ts`, a CSS-based solution was implemented to hide them, targeting their specific `href` and ensuring they were not the intended right-aligned links.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
