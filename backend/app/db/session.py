import re
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

_async_engine = None
_async_session_local = None

def get_async_engine():
    global _async_engine
    if _async_engine is None:
        # Strip query parameters from the DATABASE_URL
        database_url_without_params = re.sub(r"\?.*$", "", settings.DATABASE_URL)
        
        _async_engine = create_async_engine(
            database_url_without_params, 
            echo=True,
            connect_args={"ssl": True} # Correctly enable SSL for asyncpg
        )
    return _async_engine

def get_async_session_local():
    global _async_session_local
    if _async_session_local is None:
        _async_session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=get_async_engine(), class_=AsyncSession
        )
    return _async_session_local

async def get_db():
    async with get_async_session_local()() as session:
        yield session