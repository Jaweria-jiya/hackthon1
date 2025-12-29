# Data Model for Physical AI & Humanoid Robotics Book

This document defines the data models for the key entities in the project.

## 1. Book Chapter

Represents a single chapter of the book.

-   **chapter_id** (string, primary key): Unique identifier for the chapter.
-   **module** (string): The module the chapter belongs to (e.g., "The Robotic Nervous System (ROS 2)").
-   **title** (string): The title of the chapter.
-   **content_markdown** (string): The full Markdown content of the chapter.

## 2. Chatbot Query

Represents a user's question to the RAG chatbot.

-   **query_id** (string, primary key): Unique identifier for the query.
-   **session_id** (string): Identifier for the user's session.
-   **query_text** (string): The text of the user's question.
-   **timestamp** (datetime): The time the query was submitted.

## 3. Chatbot Response

Represents the chatbot's answer.

-   **response_id** (string, primary key): Unique identifier for the response.
-   **query_id** (string, foreign key): The ID of the query this response is for.
-   **response_text** (string): The text of the chatbot's answer.
-   **citations** (array of strings): A list of source identifiers from the book content that were used to generate the response.
-   **timestamp** (datetime): The time the response was generated.
