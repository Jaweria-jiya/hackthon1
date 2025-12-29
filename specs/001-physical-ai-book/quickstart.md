# Quickstart

This guide provides the steps to set up and run the "Physical AI & Humanoid Robotics Book" project.

## Prerequisites

-   Node.js 20.x or later
-   Python 3.11 or later
-   Git

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

## 2. Set up environment variables

Copy the `.env.example` file to a new file named `.env` and fill in the required values.

```bash
cp .env.example .env
```

## 3. Install dependencies

### Backend

```bash
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend-docusaurus
npm install
```

## 4. Run the application

### Backend

```bash
uvicorn main:app --reload
```

The backend server will be running at `http://localhost:8000`.

### Frontend

```bash
cd frontend-docusaurus
npm start
```

The Docusaurus development server will be running at `http://localhost:3000`.

## 5. Ingest data

To populate the Qdrant vector database with the book's content, run the ingestion script:

```bash
python data/ingest/ingest_chapters.py
```
