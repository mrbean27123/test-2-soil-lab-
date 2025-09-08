from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from database.session import async_postgresql_session_factory


async def get_postgresql_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a new asynchronous database session.

    Used as a FastAPI dependency to inject an AsyncSession into request handlers. The session is
    automatically closed when the request is completed.
    """
    async with async_postgresql_session_factory() as session:
        yield session


@asynccontextmanager
async def get_postgresql_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an async context-managed database session.

    Useful for manual session control outside FastAPI, such as in scripts or background tasks.
    """
    async with async_postgresql_session_factory() as session:
        yield session
