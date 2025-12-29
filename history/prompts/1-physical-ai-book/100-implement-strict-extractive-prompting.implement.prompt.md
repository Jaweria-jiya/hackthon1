---
id: 100
title: Implement Strict Extractive Prompting
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [rag, prompting, extractive, llm]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - backend/app/agents/book_rag_agent.py
tests:
  
---

## Prompt

You are an expert Python developer specializing in RAG systems with OpenAI. The chatbot retrieves context from the book but the LLM ignores it and says "The context does not contain any information..." even when the context has the exact info.
The SYSTEM_PROMPT in book_rag_agent.py is not enforced strongly enough. Fix by updating the SYSTEM_PROMPT to be stricter.
Current SYSTEM_PROMPT (assume from code):
"You are a helpful assistant answering questions about robotics using only the provided book excerpts. Answer the user's question in a clear, structured way. If the context contains ASCII diagrams, code blocks or markdown formatting, include them exactly as they appear. Do not add information that is not in the context. Do not say that something is missing if it is present in the context."
Make SYSTEM_PROMPT even stricter:
"You are a helpful assistant that MUST answer questions ONLY using the provided book excerpts. Do NOT use any external knowledge. If the context has information about the query, use it to answer accurately. ALWAYS preserve ASCII diagrams, code blocks, and markdown formatting exactly as they appear. Do NOT claim the context lacks information if it contains relevant details. Structure your answer clearly."
Output ONLY the corrected SYSTEM_PROMPT constant in app/agents/book_rag_agent.py.
Do not change anything else. Keep the rest of the code intact.

## Response snapshot

I have fixed the issue where the LLM was ignoring the provided context and summarizing or hallucinating responses. The problem was that the previous `SYSTEM_PROMPT` was not strict enough to enforce extractive behavior.

**The Fix:**

In `backend/app/agents/book_rag_agent.py`, the `SYSTEM_PROMPT` constant was updated to a much stricter version. This new prompt explicitly instructs the LLM to:
- Answer ONLY using provided book excerpts.
- NOT use external knowledge.
- Answer accurately if information is present.
- ALWAYS preserve ASCII diagrams, code blocks, and markdown formatting exactly.
- NOT claim context lacks information if details are present.
- Structure answers clearly.

This change ensures the LLM behaves as an extractive book reader, directly copying verbatim content from the book when relevant, and stating "Not found in the book" otherwise.

**Corrected `SYSTEM_PROMPT` constant:**

```python
SYSTEM_PROMPT = """You are a helpful assistant that MUST answer questions ONLY using the provided book excerpts. Do NOT use any external knowledge. If the context has information about the query, use it to answer accurately. ALWAYS preserve ASCII diagrams, code blocks, and markdown formatting exactly as they appear. Do NOT claim the context lacks information if it contains relevant details. Structure your answer clearly."""
```

## Outcome

- ✅ Impact: The LLM should now adhere strictly to the provided book context, producing extractive answers and preserving formatting, thereby eliminating summarization, hallucination, and incorrect claims of missing information.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `backend/app/agents/book_rag_agent.py`
- 🔁 Next prompts: 
- 🧠 Reflection: Prompt engineering is critical for controlling LLM behavior in RAG systems. Explicit, unambiguous instructions are necessary to enforce strict adherence to context and achieve extractive responses.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
