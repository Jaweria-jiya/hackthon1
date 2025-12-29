---
id: 106
title: Clean Book Frontpage by Removing UI Containers
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement
labels: ["refactor", "frontpage-cleanup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/docs/learning-roadmap.md (modified)
 - frontend-docusaurus/website/docs/roadmap/week-1-2.md (deleted)
 - frontend-docusaurus/website/docs/roadmap/week-3-5.md (deleted)
 - frontend-docusaurus/website/docs/roadmap/week-6-10.md (deleted)
 - frontend-docusaurus/website/docs/roadmap/week-11-13.md (deleted)
 - frontend-docusaurus/website/docs/roadmap/_category_.json (deleted)
tests:
 - No tests were run or added.
---

## Prompt

/sp.implement 🎯 TASK

You are a DOCUMENT CLEANUP & STRUCTURE PRESERVER.

Your task is to clean the book frontpage by removing specific UI-style containers and links, while preserving the remaining content layout and readability.

🧹 REMOVE (MANDATORY)

Completely and permanently remove ALL of the following from the frontpage:

Any card / container / box / grid layout, including but not limited to:

“13-Week Guided Learning Program” section

Week-based cards such as:

“Weeks 1–2 → Foundations”

“Weeks 3–5 → ROS 2 Core”

“Weeks 6–10 → Simulation & Isaac”

“Weeks 11–13 → Humanoids & Conversational AI”

Their headings, subheadings, labels, and descriptions

ALL links related to those containers, including:

“See full roadmap →”

Any page or section that opens when those links are clicked

➡️ These linked pages must be deleted entirely, not just unlinked.

🛑 STRICT RULES (VERY IMPORTANT)

❌ Do NOT replace removed sections with summaries
❌ Do NOT add new headings
❌ Do NOT invent alternative content
❌ Do NOT mention weeks, timelines, or roadmaps
❌ Do NOT leave visual gaps or broken spacing

🧱 LAYOUT MAINTENANCE RULES

After removal:

Reflow the remaining content naturally

Fix spacing so the page does NOT look empty or broken

Maintain:

consistent margins

clean typography

smooth visual flow

If two sections become adjacent after deletion, merge spacing cleanly

The page must look like the containers never existed.

📖 CONTENT PRESERVATION RULE

✔ Keep ALL existing non-container text exactly as it is
✔ Preserve original order
✔ Preserve tone and structure

Only layout cleanup is allowed — no content rewriting.

🔍 FINAL SELF-CHECK (MANDATORY)

Before finishing, verify:

No “Week”, “Roadmap”, or “Program” wording remains

No clickable “See full roadmap →” links exist

No orphan empty sections remain

Frontpage looks clean, professional, and intentional

If anything remains that references the removed containers → delete it.

## Response snapshot

Successfully cleaned the book frontpage by removing specified UI containers and linked roadmap content, ensuring content layout and readability are preserved.

## Outcome

- ✅ Impact: Cleaned up book frontpage, removing UI containers and linked roadmap files as specified, enhancing readability and compliance with design rules.
- 🧪 Tests: No automated tests were run for this visual and content refactoring task.
- 📁 Files: Modified `learning-roadmap.md` and deleted multiple files in the `docs/roadmap/` directory.
- 🔁 Next prompts: Awaiting further instructions on code implementation of RAG answering rules or other tasks.
- 🧠 Reflection: Successfully executed the document cleanup task according to strict rules, including content removal, layout maintenance, and deletion of linked files. The process involved precise markdown manipulation to ensure no visual gaps or unwanted content remained.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
