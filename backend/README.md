# Backend - Physical AI & Humanoid Robotics Book

This directory contains the FastAPI backend for the Physical AI & Humanoid Robotics Book project.

## Setup

1.  **Create a Python Virtual Environment**:
    ```bash
    python -m venv venv
    ```

2.  **Activate the Virtual Environment**:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**:
    Create a `.env` file in the `backend/` directory by copying `.env.example` and filling in the necessary values, especially `DATABASE_URL`.
    ```bash
    cp .env.example .env
    ```

## Running the Application

To run the FastAPI application, make sure your virtual environment is activated and then execute:
```bash
uvicorn app.main:app --reload
```
The application will be accessible at `http://127.0.0.1:8000` (or `http://localhost:8000`).

## Database Migrations (Alembic)

1.  **Initialize Alembic (if not already initialized)**:
    ```bash
    alembic init -t async alembic
    ```

2.  **Generate a Migration**:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```

3.  **Apply Migrations**:
    ```bash
    alembic upgrade head
    ```
