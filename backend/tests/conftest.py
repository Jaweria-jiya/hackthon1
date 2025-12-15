import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from app.db.base import Base
from app.db.session import get_db
from app.main import app
import pytest_asyncio # Import pytest_asyncio

# Load environment variables from .env.test for testing purposes
load_dotenv(dotenv_path=".env.test")

# Use an in-memory SQLite database for testing
# For async, SQLite with check_same_thread=False is generally not recommended as it's sync-only,
# but for testing simple cases, we'll configure it.
# Ideally, for async tests, you'd use an async DB like PostgreSQL with asyncpg.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=False
)
AsyncTestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

@pytest_asyncio.fixture(name="db_session") # Use pytest_asyncio.fixture
async def db_session_fixture():
    # Create the database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncTestingSessionLocal() as session:
        yield session
        
        # Drop the database tables
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(name="client") # Use pytest_asyncio.fixture
async def client_fixture(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()