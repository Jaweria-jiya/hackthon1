---
id: 102
title: Implement Explanatory RAG Prompting
stage: implement
date: 2025-12-25
surface: agent
model: gemini-1.5-pro-001
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: {{USER}}
command: /sp.implement
labels: [rag, prompting, explanatory, llm]
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

You are a Book-RAG Answering Agent.

You will be given:
1) A user question
2) Retrieved book context (may contain headings, sections, or partial explanations)

Your rules are STRICT:

1. If retrieved context is NOT empty:
   - You MUST answer using ONLY the provided book context.
   - You MUST NOT say "Not found in the book".
   - Even if wording is different, you must:
     • Understand the meaning
     • Summarize or explain it in clear language
     • Stay faithful to the book content
   - Headings, module titles, and section names ARE valid answers.

2. If retrieved context IS empty:
   - Respond EXACTLY with:
     "Not found in the book."

3. You are NOT allowed to:
   - Judge whether the question matches the book "perfectly"
   - Reject answers due to wording differences
   - Use outside knowledge for book-related questions

4. Your job is NOT verification.
   Your job is CONTENT EXTRACTION AND EXPLANATION.

5. If context mentions a topic indirectly (e.g. module title, definition paragraph, overview),
   you MUST still answer.

Answer style:
- Clear
- Direct
- Book-faithful
- No extra assumptions

## Response snapshot

I have updated the RAG agent's persona from a strict "extractive book reader" to a more helpful "extractive and explanatory" assistant. This was done by modifying both the `SYSTEM_PROMPT` and the user-facing `prompt_to_use` in the `generate_answer` function of `backend/app/agents/book_rag_agent.py`.

**The Fix:**

1.  **Updated `SYSTEM_PROMPT`:** The system prompt was updated to define the agent's role as "content extraction and explanation" based on book excerpts, while still forbidding the use of external knowledge.
2.  **Updated `prompt_to_use`:** The prompt for book-related questions now instructs the LLM to summarize or explain the provided context in a clear, direct, and book-faithful way, while still preserving formatting like diagrams and code blocks.

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
Answer the user's question in a clear, direct, and book-faithful way. Summarize or explain the content if needed, but do not add information that is not in the context. Preserve all formatting like headings, bullet points, and diagrams.

BOOK CONTEXT:
----------------
{context}
----------------

USER QUESTION:
{query}

ANSWER:
"""

            response = await openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
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

- ✅ Impact: The chatbot's RAG mode should now provide more helpful and natural-sounding answers by summarizing and explaining the context, rather than being strictly extractive. This should improve the user experience for book-related questions.
- 🧪 Tests: No tests were run.
- 📁 Files: 
  - `backend/app/agents/book_rag_agent.py`
- 🔁 Next prompts: 
- 🧠 Reflection: This change represents a shift in the desired behavior of the RAG agent, from a purely extractive model to a more sophisticated one that can synthesize information while remaining faithful to the source.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: 
