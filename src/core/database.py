"""
Database module for Fast Zero application.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)


# pragma: no cover
async def get_session():
    """Returns a new database session."""
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
