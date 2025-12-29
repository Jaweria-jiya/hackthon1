# Production-Ready API Integration and Setup Instructions

This document provides the final code and instructions to integrate the frontend and backend of the application, including the chatbot.

## 1. Environment Setup

1.  **Create a `.env` file** in the root of the project by copying the `.env.template` file.

    ```bash
    cp .env.template .env
    ```

2.  **Update the `.env` file** with your specific configurations for the database, secret keys, and API keys.

    ```dotenv
    # Backend Configuration
    DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname"
    SECRET_KEY="your_super_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Gemini API Key for Chatbot
    GEMINI_API_KEY="your_gemini_api_key"

    # Qdrant Configuration for RAG
    QDRANT_URL="http://localhost:6333"
    QDRANT_API_KEY=""

    # Frontend Configuration
    REACT_APP_API_BASE_URL="http://localhost:8000/api"
    REACT_APP_FRONTEND_URL="http://localhost:3000"
    ```

## 2. Backend Setup and Execution

1.  **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2.  **Install the required Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the FastAPI backend server:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The backend will be available at `http://localhost:8000`.

## 3. Frontend Setup and Execution

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend-docusaurus/website
    ```

2.  **Install the required Node.js dependencies:**

    ```bash
    npm install
    ```

3.  **Run the Docusaurus frontend development server:**

    ```bash
    npm start
    ```

    The frontend will be available at `http://localhost:3000`.

## 4. Summary of Changes

### Backend

*   **Environment Variables:** The backend now uses a `.env` file and `pydantic-settings` for configuration management (`backend/app/core/config.py`).
*   **CORS:** The CORS middleware in `backend/app/main.py` is now configured to only allow requests from the frontend URL specified in the `.env` file.
*   **Chatbot Endpoint:** The RAG endpoint has been moved to `backend/app/api/rag/chat.py` and is now available at `/api/chat/query`.

### Frontend

*   **API Configuration:** The frontend now retrieves the backend API URL from the `customFields` in `docusaurus.config.ts`, which is populated from the `.env` file.
*   **API Services:** A new API service module has been created at `frontend-docusaurus/website/src/services/api.ts`. This module centralizes all API calls to the backend.
*   **Authentication Context:** The application is now wrapped with an `AuthProvider` in `frontend-docusaurus/website/src/theme/Root.tsx` to provide global authentication state.

This setup ensures a clean separation of concerns and a secure, production-ready integration between the frontend, backend, and chatbot services.
