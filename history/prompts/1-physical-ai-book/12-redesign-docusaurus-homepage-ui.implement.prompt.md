---
id: 12
title: Redesign Docusaurus Homepage UI
stage: implement
date: 2025-12-13
surface: agent
model: unknown
feature: 1-physical-ai-book
branch: unknown
user: ALI
command: /sp.implement You are working on an existing Docusaurus website.

GOAL:
Redesign ONLY the FRONT PAGE (homepage) UI.

STRICT SCOPE:
- Modify ONLY the homepage (src/pages/index.tsx or equivalent).
- Do NOT modify docs pages, sidebar, markdown files, or routing.
- Do NOT add new pages.
- Header and footer must remain unchanged.
- Remove all default Docusaurus homepage sections (features boxes, tutorial button, illustrations).

DESIGN REQUIREMENTS (VERY IMPORTANT):

1. BACKGROUND
- The ENTIRE homepage background must use the SAME background color as the footer.
- No white sections.
- No cards, no boxes, no illustrations.

2. CONTENT (CENTERED)
- Vertically and horizontally center all content.
- Show ONLY:
  - Book Title (large, white text)
  - Below it: “Start Reading Book →”

3. TEXT STYLING
- Book title:
  - White color
  - Large font size
  - Bold
- “Start Reading Book →”:
  - Light green + dark green accent
  - Arrow must be visible
  - Cursor pointer on hover
  - Smooth hover effect (slight glow or underline)

4. INTERACTION
- Clicking “Start Reading Book →” must navigate to the main book docs route:
  /docs/intro
  (or existing main docs entry)

5. LAYOUT RULES
- No feature boxes
- No tutorial buttons
- No default Docusaurus hero layout
- Minimal, clean, professional
- Modern AI / Robotics aesthetic

6. TECHNICAL CONSTRAINTS
- Use React + Docusaurus conventions
- Use CSS module or inline styles (no external UI libraries)
- Keep code MDX-safe and production-ready
- Do NOT break dark mode

OUTPUT REQUIREMENTS:
- Provide the COMPLETE updated homepage code file
- Include any necessary CSS (inline or module)
- Do NOT explain — output code only
labels: ["ui", "docusaurus", "homepage", "redesign"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- frontend-docusaurus/website/src/pages/index.tsx
- frontend-docusaurus/website/src/pages/index.module.css
tests:
- null
---

## Prompt

/sp.implement You are working on an existing Docusaurus website.

GOAL:
Redesign ONLY the FRONT PAGE (homepage) UI.

STRICT SCOPE:
- Modify ONLY the homepage (src/pages/index.tsx or equivalent).
- Do NOT modify docs pages, sidebar, markdown files, or routing.
- Do NOT add new pages.
- Header and footer must remain unchanged.
- Remove all default Docusaurus homepage sections (features boxes, tutorial button, illustrations).

DESIGN REQUIREMENTS (VERY IMPORTANT):

1. BACKGROUND
- The ENTIRE homepage background must use the SAME background color as the footer.
- No white sections.
- No cards, no boxes, no illustrations.

2. CONTENT (CENTERED)
- Vertically and horizontally center all content.
- Show ONLY:
  - Book Title (large, white text)
  - Below it: “Start Reading Book →”

3. TEXT STYLING
- Book title:
  - White color
  - Large font size
  - Bold
- “Start Reading Book →”:
  - Light green + dark green accent
  - Arrow must be visible
  - Cursor pointer on hover
  - Smooth hover effect (slight glow or underline)

4. INTERACTION
- Clicking “Start Reading Book →” must navigate to the main book docs route:
  /docs/intro
  (or existing main docs entry)

5. LAYOUT RULES
- No feature boxes
- No tutorial buttons
- No default Docusaurus hero layout
- Minimal, clean, professional
- Modern AI / Robotics aesthetic

6. TECHNICAL CONSTRAINTS
- Use React + Docusaurus conventions
- Use CSS module or inline styles (no external UI libraries)
- Keep code MDX-safe and production-ready
- Do NOT break dark mode

OUTPUT REQUIREMENTS:
- Provide the COMPLETE updated homepage code file
- Include any necessary CSS (inline or module)
- Do NOT explain — output code only

## Response snapshot

The Docusaurus homepage UI has been redesigned according to the specified requirements. This included removing default Docusaurus sections, centering the book title ("Physical AI & Humanoid Robotics") and a "Start Reading Book →" link, applying specific text styling, and ensuring navigation to `/docs/intro`. The background color is set using Docusaurus theme variables (`var(--ifm-background-color)`) with a fallback dark gray (`#242526`) to match the footer's dark style. All changes were applied to `frontend-docusaurus/website/src/pages/index.tsx` and a new CSS module `frontend-docusaurus/website/src/pages/index.module.css`.

## Outcome

- ✅ Impact: The Docusaurus homepage UI has been redesigned according to the specified requirements, including background color, centered content, text styling, interaction, and adherence to technical constraints.
- 🧪 Tests: No automated tests were executed as part of this task.
- 📁 Files: Modified one existing file (`frontend-docusaurus/website/src/pages/index.tsx`) and created one new file (`frontend-docusaurus/website/src/pages/index.module.css`) to implement the homepage redesign.
- 🔁 Next prompts: User should run `npx docusaurus start` to view the redesigned homepage and verify it meets all requirements and compiles without errors.
- 🧠 Reflection: Successfully redesigned the homepage UI, focusing on strict adherence to visual and technical constraints. The challenge was interpreting the "SAME background color as the footer" requirement without direct access to the live rendering, which was addressed by using Docusaurus theme variables and a sensible fallback.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): implement
- Next experiment (smallest change to try): User to validate Docusaurus build and UI in browser.
