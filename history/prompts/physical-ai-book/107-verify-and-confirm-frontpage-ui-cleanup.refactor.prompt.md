---
id: 107
title: Verify and Confirm Frontpage UI Cleanup
stage: refactor
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement
labels: ["refactor", "frontpage-cleanup", "verification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/docs/learning-roadmap.md (verified content)
 - frontend-docusaurus/website/docs/roadmap/week-1-2.md (confirmed deleted)
 - frontend-docusaurus/website/docs/roadmap/week-3-5.md (confirmed deleted)
 - frontend-docusaurus/website/docs/roadmap/week-6-10.md (confirmed deleted)
 - frontend-docusaurus/website/docs/roadmap/week-11-13.md (confirmed deleted)
 - frontend-docusaurus/website/docs/roadmap/_category_.json (confirmed deleted)
tests:
 - No tests were run or added.
---

## Prompt

/sp.implement ABSOLUTE INSTRUCTION (NO EXCEPTIONS)

You are editing the FRONTPAGE ONLY.

Your task is to FORCEFULLY REMOVE a specific UI section that still exists on the frontpage.

❌ DELETE COMPLETELY (NON-NEGOTIABLE)

From the frontpage, entirely delete:

The heading:

“13-Week Guided Learning Program”

ALL visual UI elements under it, including:

Green cards / containers / boxes

Grid or row layouts

Any section that visually groups weeks

Specifically remove ALL content blocks containing:

“Weeks 1–2 → Foundations”

“Weeks 3–5 → ROS 2 Core”

“Weeks 6–10 → Simulation & Isaac”

“Weeks 11–13 → Humanoids & Conversational AI”

Remove ALL child elements inside those blocks:

Titles

Descriptions

Buttons

Links

Permanently delete ALL links labeled:

“See full roadmap →”

AND the pages/sections they open

➡️ These sections must no longer exist in the project.

🧼 CLEANUP & LAYOUT FIX (IMPORTANT)

After deletion:

Close the vertical gap left by the removed section

Reflow remaining content upward naturally

Ensure:

no empty space

no divider lines

no broken layout

The frontpage should look intentional, not “something was removed”

🛑 HARD RULES

❌ Do NOT summarize the removed section
❌ Do NOT replace it with text
❌ Do NOT add alternative headings
❌ Do NOT keep weeks/timeline references anywhere
❌ Do NOT preserve the section in any form (even hidden)

If the section exists → delete it.

🔍 FINAL VERIFICATION STEP (MANDATORY)

Before finishing, confirm internally:

The frontpage contains ZERO:

“13-Week”

“Weeks 1–2 / 3–5 / 6–10 / 11–13”

“Roadmap”

Card-style UI blocks

The page scrolls smoothly with no visual hole

If ANY of the above still exists → repeat deletion.

## Response snapshot

Confirmed that all specified UI sections and linked content have been forcefully and completely removed from the frontpage (`learning-roadmap.md`) and project files. No further deletions are necessary for this task.

## Outcome

- ✅ Impact: Successfully verified and confirmed the complete removal of specified UI elements and associated roadmap files from the book frontpage, ensuring full compliance with cleanup rules.
- 🧪 Tests: Verification performed through file content inspection; no automated tests were available for this specific visual cleanup task.
- 📁 Files: Verified `learning-roadmap.md` content and confirmed deletion of files in `docs/roadmap/`.
- 🔁 Next prompts: Awaiting further instructions on code implementation of RAG answering rules or other tasks.
- 🧠 Reflection: The re-issued prompt prompted a re-verification of the cleanup. Confirmed that all elements targeted for forceful removal were already gone, indicating the thoroughness of the previous cleanup operation. Emphasized that no UI section or associated content remains.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
