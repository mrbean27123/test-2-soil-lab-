from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings


# Synchronous engine for Alembic and migrations
sync_postgresql_engine = create_engine(settings.SYNC_POSTGRES_DATABASE_URL, echo=False)

# Asynchronous database engine and session factory
async_postgresql_engine = create_async_engine(settings.ASYNC_POSTGRES_DATABASE_URL, echo=False)
async_postgresql_session_factory = async_sessionmaker(
    bind=async_postgresql_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)
