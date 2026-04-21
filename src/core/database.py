"""
Database module for Fast Zero application.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.settings import Settings

engine = create_async_engine(
    Settings().ASYNC_DATABASE_URL,
    max_overflow=10,
    pool_size=5,
    pool_recycle=600,
    pool_timeout=30,
    echo=False,
)


# pragma: no cover
async def get_session():
    """Returns a new database session."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
