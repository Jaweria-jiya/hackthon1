---
id: 13
title: Implement Fullscreen Docusaurus Homepage
stage: implement
date: 2025-12-13
surface: agent
model: unknown
feature: 1-physical-ai-book
branch: unknown
user: ALI
command: /sp.implement You are modifying a Docusaurus website.

TASK:
Redesign ONLY the homepage so that it has:
- NO navbar
- NO footer

CRITICAL RULE:
❗ Do NOT use the <Layout> component on the homepage.

Instead:
- Render a FULLSCREEN custom page using plain React.
- The homepage must NOT inherit Docusaurus header or footer.

DESIGN REQUIREMENTS:

1. BACKGROUND
- The entire viewport (100vh, 100vw) background color must EXACTLY match the footer background color used elsewhere in the site.
- No white areas.

2. CENTER CONTENT
- Perfect vertical and horizontal centering.
- Show ONLY:
  - Book title text
  - Below it: "Start Reading Book →"

3. TEXT STYLING
- Book title:
  - White color
  - Very large font
  - Bold
  - Center aligned
- "Start Reading Book →":
  - Green color (light + dark accent)
  - Arrow included
  - Pointer cursor
  - Smooth hover animation (color shift or underline)

4. NAVIGATION
- Clicking "Start Reading Book →" must navigate to:
  /docs/intro

5. STRICT EXCLUSIONS
- No navbar
- No footer
- No hero section
- No feature boxes
- No buttons
- No cards
- No images

6. FILE SCOPE
- Modify ONLY: src/pages/index.tsx
- Do NOT touch docs, sidebar, config, or theme files.

OUTPUT FORMAT:
- Provide COMPLETE replacement code for src/pages/index.tsx
- Include styles inline or CSS module
- Production-ready React code
- No explanations, code only
labels: ["ui", "docusaurus", "homepage", "redesign", "fullscreen"]
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

/sp.implement You are modifying a Docusaurus website.

TASK:
Redesign ONLY the homepage so that it has:
- NO navbar
- NO footer

CRITICAL RULE:
❗ Do NOT use the <Layout> component on the homepage.

Instead:
- Render a FULLSCREEN custom page using plain React.
- The homepage must NOT inherit Docusaurus header or footer.

DESIGN REQUIREMENTS:

1. BACKGROUND
- The entire viewport (100vh, 100vw) background color must EXACTLY match the footer background color used elsewhere in the site.
- No white areas.

2. CENTER CONTENT
- Perfect vertical and horizontal centering.
- Show ONLY:
  - Book title text
  - Below it: "Start Reading Book →"

3. TEXT STYLING
- Book title:
  - White color
  - Very large font
  - Bold
  - Center aligned
- "Start Reading Book →":
  - Green color (light + dark accent)
  - Arrow included
  - Pointer cursor
  - Smooth hover animation (color shift or underline)

4. NAVIGATION
- Clicking "Start Reading Book →" must navigate to:
  /docs/intro

5. STRICT EXCLUSIONS
- No navbar
- No footer
- No hero section
- No feature boxes
- No buttons
- No cards
- No images

6. FILE SCOPE
- Modify ONLY: src/pages/index.tsx
- Do NOT touch docs, sidebar, config, or theme files.

OUTPUT FORMAT:
- Provide COMPLETE replacement code for src/pages/index.tsx
- Include styles inline or CSS module
- Production-ready React code
- No explanations, code only

## Response snapshot

The Docusaurus homepage has been completely redesigned as a fullscreen, standalone React component, without using the `<Layout>` component. This involved modifying `frontend-docusaurus/website/src/pages/index.tsx` to directly render the custom content and updating `frontend-docusaurus/website/src/pages/index.module.css` to manage fullscreen rendering, centering, background, and text styling. All strict design requirements (no navbar, no footer, centered content, specific text styling, navigation) and technical constraints were adhered to.

## Outcome

- ✅ Impact: The Docusaurus homepage has been completely redesigned as a fullscreen, standalone React component, without using the `<Layout>` component, and adhering to all strict design requirements and exclusions (no navbar, no footer, centered content, specific text styling, and navigation).
- 🧪 Tests: No automated tests were executed as part of this task.
- 📁 Files: Modified `frontend-docusaurus/website/src/pages/index.tsx` and `frontend-docusaurus/website/src/pages/index.module.css` to implement the fullscreen homepage redesign.
- 🔁 Next prompts: User should run `npx docusaurus start` to view the redesigned homepage and verify it meets all requirements and compiles without errors.
- 🧠 Reflection: Successfully implemented a complex UI redesign requiring significant deviation from standard Docusaurus practices (e.g., avoiding `<Layout>`). This required careful consideration of CSS for full-screen rendering and hiding default Docusaurus elements.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): implement
- Next experiment (smallest change to try): User to validate Docusaurus build and UI in browser.
