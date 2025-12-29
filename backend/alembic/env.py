import os
from logging.config import fileConfig

from sqlalchemy import pool, create_engine
from app.core.config import settings
from dotenv import load_dotenv
from loguru import logger

from alembic import context

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app.db.base import Base
from app.db import models # Import all models here
target_metadata = Base.metadata

def get_db_url() -> str:
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite"):
        logger.warning(
            "Alembic is running with a SQLite DATABASE_URL. "
            "This is usually not intended for production migrations."
        )
        return db_url
    
    if "asyncpg" in db_url:
        db_url = db_url.replace("+asyncpg", "+psycopg2")
        logger.info(f"Converted async DATABASE_URL to sync for Alembic: {db_url}")
    return db_url

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_db_url()
    if url == "sqlite:///./invalid_db.db":
        logger.error("Cannot run migrations offline: DATABASE_URL is invalid or contains placeholders.")
        exit(1)
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        get_db_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
