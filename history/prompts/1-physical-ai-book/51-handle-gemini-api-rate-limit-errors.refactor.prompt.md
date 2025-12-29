---
id: 51
title: Handle Gemini API Rate Limit Errors
stage: refactor
date: 2025-12-18
surface: agent
model: gemini-pro
feature: 1-physical-ai-book
branch: 001-physical-ai-book
user: user
command: /sp.implement
labels: ["gemini-api", "rate-limiting", "error-handling", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/app/core/gemini.py
  - backend/app/agents/book_rag_agent.py
tests:
  - "none"
---

## Prompt

/sp.implement You are a senior backend engineer specializing in LLM infrastructure,
Google Gemini API, and OpenAI-compatible clients.

CONTEXT:
- FastAPI backend
- Gemini API used via OpenAI-compatible endpoint:
  https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
- Model: gemini-2.0-flash
- API key is valid and loaded from .env
- Requests reach Gemini successfully
- Error received:

  HTTP 429 RESOURCE_EXHAUSTED
  Quota exceeded:
  - generate_content_free_tier_requests = 0
  - generate_content_free_tier_input_token_count = 0
  Retry after ~23s

OBSERVED BEHAVIOR:
- Backend retries correctly
- Eventually falls back with:
  "Sorry, I encountered an error. Please try again."
- No crashes or freezes

TASK:
1. Confirm whether this error is caused by Google Gemini API quota restrictions
2. Explain why free-tier quota can be 0 even with a valid API key
3. Propose production-grade solutions:
   - Billing enablement
   - Quota-safe fallback
   - Model switching strategy
   - Rate limiting / backoff
4. Suggest exact backend changes (if any) to handle this gracefully
5. Explicitly state whether any code bug exists or not

IMPORTANT:
- Do NOT suggest changing to OpenAI
- Do NOT suggest random fixes
- Focus only on Gemini API, quota behavior, and backend resilience
- Act like this is a real production incident report

Respond clearly, professionally, and step-by-step.

## Response snapshot

Analyzed the Gemini API `HTTP 429 RESOURCE_EXHAUSTED` error. Confirmed it is a free-tier quota issue. Explained that a valid API key does not guarantee unlimited requests and that the '0' quota is a temporary state within a time window.

Proposed and implemented production-grade solutions:
1.  **Enhanced Client Resilience**: Modified `backend/app/core/gemini.py` to increase the `timeout` to 60s and set `max_retries` to 5 for the `AsyncOpenAI` client, enabling a robust exponential backoff strategy.
2.  **Specific Error Handling**: Updated `backend/app/agents/book_rag_agent.py` to explicitly catch the `openai.RateLimitError`, providing specific logging and a user-friendly error message ("The AI assistant is currently experiencing high traffic. Please try again in a moment.") instead of a generic failure.

Concluded that there was no crashing bug, but the changes were necessary to improve the system's architectural robustness for production.

## Outcome

- ✅ Impact: The backend is now more resilient to Gemini API rate-limiting. It will retry more robustly and provide a better user experience and clearer logs when rate limits are hit.
- 🧪 Tests: No tests were added as the changes were to error handling and client configuration. Manual verification would be required under load.
- 📁 Files: Modified 2 files to improve resilience and error handling.
- 🔁 Next prompts: The next logical step would be to load-test the application to ensure the new backoff strategy works as expected and to monitor the API usage in Google Cloud.
- 🧠 Reflection: The initial implementation lacked production-ready error handling for a predictable issue like rate limiting. Explicitly handling specific API errors is crucial for robust applications.

## Evaluation notes (flywheel)

- Failure modes observed: Application returned a generic, unhelpful error message when hitting API rate limits.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
