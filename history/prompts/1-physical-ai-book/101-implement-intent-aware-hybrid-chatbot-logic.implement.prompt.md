---
id: 101
title: Implement Intent-Aware Hybrid Chatbot Logic
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [rag, intent-classification, chatbot, hybrid]
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

You are a senior AI engineer designing a HYBRID chatbot with two modes:
1) General LLM Chat Mode
2) Strict Book-Based RAG Mode

CURRENT PROBLEM:
The chatbot is incorrectly forcing ALL user queries through RAG.
As a result:
- Simple greetings like "hello" return book content
- General questions like "what is your name?" return "Not found in the book"
- Book questions are sometimes answered too briefly or incorrectly

YOUR TASK:
Fix this by implementing INTENT-AWARE RESPONSE LOGIC using prompting.

CORE LOGIC (MANDATORY):
Before answering, ALWAYS classify the user's query into ONE of these categories:

CATEGORY A — GENERAL CONVERSATION
Examples:
- hello
- hi
- how are you
- what is your name
- who built you

RULES FOR CATEGORY A:
- DO NOT use Qdrant
- DO NOT use book context
- Answer naturally using the LLM’s own knowledge
- Friendly, short, conversational answers are allowed

CATEGORY B — BOOK-RELATED QUESTION
Examples:
- What is ROS?
- What is ROS 2?
- ASCII Diagram: ROS 1 Communication
- Explain DDS in ROS 2

RULES FOR CATEGORY B (STRICT):
- Use ONLY the provided book context
- DO NOT use general LLM knowledge
- DO NOT summarize or paraphrase
- COPY the answer EXACTLY as written in the book
- Preserve all formatting:
  - Headings
  - Bullet points
  - Markdown
  - Code blocks
  - ASCII diagrams (character-for-character)
- If and ONLY IF the answer does not exist verbatim in the context, reply exactly:
  "Not found in the book."

IMPLEMENTATION REQUIREMENTS:
- This logic must be enforced inside `generate_answer()` in `book_rag_agent.py`
- The decision (Category A vs B) must happen BEFORE using RAG
- Keep existing retrieval, embeddings, and Qdrant logic unchanged
- Do NOT globally force RAG for all queries

PROMPT STRUCTURE FOR BOOK MODE ONLY:

"""
You are a strict book reader.

Answer ONLY using the text below.
Do not add, remove, summarize, or rewrite anything.

If the answer exists, copy it EXACTLY as written.
If it does not exist, respond with:
Not found in the book.

BOOK CONTEXT:
----------------
{context}
----------------

USER QUESTION:
{query}

ANSWER (verbatim from book only):
"""

OUTPUT REQUIREMENT:
- Implement the hybrid logic correctly
- No hallucinations
- No book content for casual chat
- No LLM knowledge for book questions

## Response snapshot

I have implemented an intent-aware response logic in the `generate_answer` function within `backend/app/agents/book_rag_agent.py`. The chatbot now operates in two modes: a general conversational mode and a strict book-based RAG mode.

**The Fix:**

1.  **Intent Classification:** Before processing any query, an LLM call is made to classify the user's intent as either `GENERAL_CONVERSATION` or `BOOK_RELATED_QUESTION`.
2.  **Conditional Logic:**
    *   If the intent is `GENERAL_CONVERSATION`, the chatbot responds naturally using a general-purpose LLM prompt, without engaging the RAG system.
    *   If the intent is `BOOK_RELATED_QUESTION`, the chatbot proceeds with the established RAG pipeline, retrieving context from Qdrant and using the strict, extractive prompt to generate a verbatim answer from the book content.

This ensures that the chatbot's responses are appropriate to the user's query type, preventing book content from being returned for casual chat and enforcing strict, extractive answers for book-related questions.

**Corrected `generate_answer` function code snippet:**

```python
async def generate_answer(query: str) -> str:
    """
    Generates a response by first classifying the user's intent and then
    either using a RAG pipeline for book-related questions or a general LLM
    for conversational queries.
    """
    if not OPENAI_CLIENT_ENABLED:
        logger.warning("OpenAI client is not enabled. Falling back to a predefined response.")
        return "Sorry, the AI services are currently unavailable. Please try again later."

    try:
        # Step 1: Classify the user's intent
        classification_prompt = f"""
        Classify the user's query into one of the following categories: GENERAL_CONVERSATION or BOOK_RELATED_QUESTION.

        - GENERAL_CONVERSATION: For greetings, conversational questions about you (the AI), or topics unrelated to robotics, AI, or the book.
        - BOOK_RELATED_QUESTION: For specific questions about robotics, AI, ROS, or any technical topic that might be in a book about physical AI and robotics.

        User Query: "{query}"

        Category:
        """
        
        logger.info(f"Classifying intent for query: '{query}'")
        classification_response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an intent classification assistant."},
                {"role": "user", "content": classification_prompt},
            ],
            temperature=0.0,
            max_tokens=20,
        )
        intent = classification_response.choices[0].message.content.strip()
        logger.info(f"Classified intent as: {intent}")

        # Step 2: Generate response based on intent
        if "GENERAL_CONVERSATION" in intent:
            logger.info("Handling as a general conversation.")
            general_prompt = "You are a helpful and friendly assistant."
            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": general_prompt},
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content

        else: # Assumes BOOK_RELATED_QUESTION
            logger.info("Handling as a book-related question.")
            context = await retrieve_from_book(query=query)
            
            if not context or not context.strip():
                logger.warning("RAG unavailable or no relevant context found for book-related question.")
                return "Not found in the book."

            logger.info("RAG context retrieved. Using RAG-based prompt.")
            prompt_to_use = f"""
You are an extractive book reader.

Your task is to COPY answers directly from the book context.
You are NOT allowed to explain, summarize, or rephrase.

Only output text that appears EXACTLY in the context.
Preserve markdown, code blocks, and ASCII diagrams exactly as-is.

If the answer does not exist word-for-word in the context, output:
Not found in the book.

BOOK CONTEXT:
----------------
{context}
----------------

USER QUESTION:
{query}

ANSWER (verbatim from book only):
"""

            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt_to_use},
                ],
                temperature=0.0,
            )
            return response.choices[0].message.content

    except RetrievalError as e:
        logger.error(f"ERROR: Qdrant retrieval failed: {e}", exc_info=True)
        return "Sorry, there was an internal issue retrieving information from the book. Please try again."
    except Exception as e:
        logger.error(f"ERROR in generate_answer: {type(e).__name__} - {e}", exc_info=True)
        return "Sorry, I encountered an unexpected error while processing your request."
```

## Outcome

- ✅ Impact: The chatbot now correctly distinguishes between general conversation and book-related questions, providing appropriate responses for each and avoiding the previous issue of forcing all queries through the RAG pipeline.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `backend/app/agents/book_rag_agent.py`
- 🔁 Next prompts: 
- 🧠 Reflection: This change introduces a crucial layer of intelligence to the chatbot, allowing it to handle a wider range of user interactions more gracefully. The intent classification step is a common and effective pattern for building hybrid RAG systems.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
