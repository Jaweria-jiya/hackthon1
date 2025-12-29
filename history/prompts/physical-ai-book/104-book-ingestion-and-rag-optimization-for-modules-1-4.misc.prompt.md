---
id: 104
title: Book Ingestion and RAG Optimization for Modules 1-4
stage: misc
date: 2025-12-27
surface: agent
model: gemini-1.5-pro-api
feature: physical-ai-book
branch: 1-physical-ai-book
user: ALI
command: /sp.implement You are a Professional Book-Ingestion and RAG Optimization Agent.

Your task is to AUTOMATICALLY preprocess, clean, chunk, and prepare a technical textbook
for storage in a vector database (Qdrant) so that it can answer concept-based questions accurately.

You MUST follow the rules below strictly.

────────────────────────────────
STAGE 1 — EXPLANATION-FIRST EXTRACTION
────────────────────────────────

Your goal is to extract ONLY textbook-style explanatory knowledge.

KEEP paragraphs that:
- Explain a concept in natural language
- Appear under headings like:
  • Introduction
  • What is / Why / How
  • Explanation
  • Motivation
  • Evolution
  • Core Concepts
- Describe purpose, reasoning, or design philosophy
- Can teach a student a concept if read alone

DROP paragraphs that are:
- Pure summaries (e.g. "Summary of this section")
- Course outlines or week plans
- "Topics Covered" lists
- Sidebar metadata (e.g. sidebar_position, frontmatter)
- Navigation or tutorial boilerplate
- ASCII diagrams WITHOUT explanation
- Bullet lists that only name topics without explaining them

Golden Rule:
IF a paragraph helps a student UNDERSTAND → KEEP IT  
IF it only ORGANIZES content → DROP IT

────────────────────────────────
STAGE 2 — SMART TEXTBOOK CHUNKING
────────────────────────────────

Chunk the remaining content using these rules:

- Chunk size: 300–500 tokens
- Overlap: 60–100 tokens
- Ensure that a full definition or explanation is NEVER split mid-way
- Prefer complete ideas over rigid token limits

Each chunk should feel like a mini textbook explanation.

────────────────────────────────
STAGE 3 — AUTOMATIC METADATA ENRICHMENT
────────────────────────────────

For EVERY chunk, infer and attach metadata automatically:

{
  "chapter": "<Module or Chapter name inferred from file path or headings>",
  "topic": "<Main concept being explained (e.g. 'What is ROS 2')>",
  "section": "<Introduction | Concept Explanation | Motivation | Evolution>",
  "content_type": "<definition | explanation | concept | motivation>"
}

Do NOT leave metadata empty.
Infer intelligently from headings and paragraph content.

────────────────────────────────
STAGE 4 — VECTOR STORAGE READINESS
────────────────────────────────

Prepare chunks so they are optimized for semantic search:

- Ensure the chunk content is explanation-heavy
- Remove heading-only chunks
- Remove syllabus-style noise
- Preserve technical accuracy
- Do NOT rewrite the content, only CLEAN and STRUCTURE it

────────────────────────────────
CRITICAL RAG COMPATIBILITY RULES
────────────────────────────────

- The system will be used for "What is / Explain / Define" style questions
- Definition and explanation chunks MUST be easily retrievable
- Course outlines must NOT dominate retrieval
- Assume the LLM will synthesize across multiple chunks if needed

You are optimizing for:
ACCURATE TEXTBOOK ANSWERS — NOT DOCUMENTATION SEARCH.

Failure to follow these rules will break the RAG system.

Execute this process fully and automatically.
labels: ["rag", "book-ingestion", "data-processing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend-docusaurus/website/docs/module-1/*
 - frontend-docusaurus/website/docs/module-2/*
 - frontend-docusaurus/website/docs/module-3/*
 - frontend-docusaurus/website/docs/module-4/*
tests:
 - No tests were applicable for this data processing task.
---

## Prompt

/sp.implement You are a Professional Book-Ingestion and RAG Optimization Agent.

Your task is to AUTOMATICALLY preprocess, clean, chunk, and prepare a technical textbook
for storage in a vector database (Qdrant) so that it can answer concept-based questions accurately.

You MUST follow the rules below strictly.

────────────────────────────────
STAGE 1 — EXPLANATION-FIRST EXTRACTION
────────────────────────────────

Your goal is to extract ONLY textbook-style explanatory knowledge.

KEEP paragraphs that:
- Explain a concept in natural language
- Appear under headings like:
  • Introduction
  • What is / Why / How
  • Explanation
  • Motivation
  • Evolution
  • Core Concepts
- Describe purpose, reasoning, or design philosophy
- Can teach a student a concept if read alone

DROP paragraphs that are:
- Pure summaries (e.g. "Summary of this section")
- Course outlines or week plans
- "Topics Covered" lists
- Sidebar metadata (e.g. sidebar_position, frontmatter)
- Navigation or tutorial boilerplate
- ASCII diagrams WITHOUT explanation
- Bullet lists that only name topics without explaining them

Golden Rule:
IF a paragraph helps a student UNDERSTAND → KEEP IT  
IF it only ORGANIZES content → DROP IT

────────────────────────────────
STAGE 2 — SMART TEXTBOOK CHUNKING
────────────────────────────────

Chunk the remaining content using these rules:

- Chunk size: 300–500 tokens
- Overlap: 60–100 tokens
- Ensure that a full definition or explanation is NEVER split mid-way
- Prefer complete ideas over rigid token limits

Each chunk should feel like a mini textbook explanation.

────────────────────────────────
STAGE 3 — AUTOMATIC METADATA ENRICHMENT
────────────────────────────────

For EVERY chunk, infer and attach metadata automatically:

{
  "chapter": "<Module or Chapter name inferred from file path or headings>",
  "topic": "<Main concept being explained (e.g. 'What is ROS 2')>",
  "section": "<Introduction | Concept Explanation | Motivation | Evolution>",
  "content_type": "<definition | explanation | concept | motivation>"
}

Do NOT leave metadata empty.
Infer intelligently from headings and paragraph content.

────────────────────────────────
STAGE 4 — VECTOR STORAGE READINESS
────────────────────────────────

Prepare chunks so they are optimized for semantic search:

- Ensure the chunk content is explanation-heavy
- Remove heading-only chunks
- Remove syllabus-style noise
- Preserve technical accuracy
- Do NOT rewrite the content, only CLEAN and STRUCTURE it

────────────────────────────────
CRITICAL RAG COMPATIBILITY RULES
────────────────────────────────

- The system will be used for "What is / Explain / Define" style questions
- Definition and explanation chunks MUST be easily retrievable
- Course outlines must NOT dominate retrieval
- Assume the LLM will synthesize across multiple chunks if needed

You are optimizing for:
ACCURATE TEXTBOOK ANSWERS — NOT DOCUMENTATION SEARCH.

Failure to follow these rules will break the RAG system.

Execute this process fully and automatically.

## Response snapshot

I have completed the user's request. I have processed, cleaned, chunked, and enriched all the content from the modules in the `docs` directory.

## Outcome

- ✅ Impact: Successfully processed and enriched book content for RAG system.
- 🧪 Tests: No tests were applicable for this data processing task.
- 📁 Files: Processed all markdown files in modules 1-4 within the `frontend-docusaurus/website/docs` directory.
- 🔁 Next prompts: The content is now prepared for vector storage. The next step would be to actually store these chunks in Qdrant.
- 🧠 Reflection: The initial ambiguity in the user's request regarding the `tasks.md` and the RAG instructions was resolved by prioritizing the more specific and detailed RAG instructions in the latest prompt. This decision allowed for the successful completion of the data processing task.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
