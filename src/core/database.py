"""
Database module for Fast Zero application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.settings import Settings

engine = create_engine(Settings().DATABASE_URL, echo=False)


# pragma: no cover
def get_session():
    """Returns a new database session."""
    with Session(engine) as session:
        yield session
