---
id: 108
title: Set Frontpage Background Image with Overlay
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement
labels: ["refactor", "frontpage-styling"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/src/pages/index.module.css (modified)
tests:
 - No tests were run or added.
---

## Prompt

/sp.implement 🔹 TASK CONTEXT

You are modifying the FRONTPAGE (homepage / landing page) of a textbook-style website.

The frontpage must remain minimal, clean, and book-like.

✅ IMAGE TO USE AS BACKGROUND

Set the following image as the frontpage background image:

https://www.shutterstock.com/image-vector/artificial-intelligence-digital-education-visualized-600nw-2653874705.jpg

🎯 BACKGROUND IMAGE RULES (VERY IMPORTANT)

Use the image only as a CSS background

Do NOT insert it as an <img> tag

Apply it to the main frontpage hero / root container

Background styling requirements:

background-size: cover

background-position: center

background-repeat: no-repeat

Ensure it scales well on desktop and mobile

🧱 CONTENT PRESERVATION (DO NOT CHANGE)

Keep exactly as-is:

Physical AI & Humanoid Robotics (main heading)

An AI-native textbook on robotics (subtitle)

Start Reading → button/link

❌ Do NOT rename
❌ Do NOT reposition
❌ Do NOT restyle text sizes

🎨 READABILITY & CONTRAST FIX

To ensure text readability:

Add a subtle dark overlay on top of the background image
(e.g. rgba(0,0,0,0.5) or equivalent)

Text must remain clearly readable on all screen sizes

🚫 STRICT DO-NOTs

Do NOT reintroduce removed sections (weekly containers)

Do NOT add gradients, animations, or extra elements

Do NOT change navigation or routing

Do NOT move content to another page

🧼 FINAL LAYOUT RESULT

After changes, the frontpage should look like:

A book cover

Clean

Minimal

Professional

With a single background image

## Response snapshot

Successfully set the frontpage background image with an overlay and applied the required styling, preserving existing content and layout.

## Outcome

- ✅ Impact: Successfully set the frontpage background image with an overlay, ensuring readability and adherence to strict styling and content preservation rules.
- 🧪 Tests: No automated tests were run for this visual styling task.
- 📁 Files: Modified `index.module.css` to apply background image and overlay.
- 🔁 Next prompts: Awaiting further instructions on code implementation of RAG answering rules or other tasks.
- 🧠 Reflection: Successfully applied the background image and overlay to the frontpage as per the explicit instructions. Ensured all styling requirements were met and content preservation rules were adhered to. The implementation was straightforward by targeting the `.fullPageWrapper` CSS class.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
