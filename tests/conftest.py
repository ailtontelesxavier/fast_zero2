"""Conftest.py - Configurações e fixtures para os testes.
Este arquivo é utilizado para definir fixtures e configurações comuns
para os testes, como a criação de um client de teste do FastAPI.
"""

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from src.core.app import app
from src.core.models import table_registry


@pytest.fixture
def client():
    """Fixture para criar um client de teste do FastAPI."""
    with TestClient(app) as client_app:
        yield client_app


@pytest.fixture
def session():
    """Fixture para criar uma sessão de banco de dados para os testes."""
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    """Context manager para mockar o tempo do
    banco de dados durante os testes."""

    def fake_time_hook(mapper, connection, target):
        target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    """Fixture para fornecer o context manager
    de mock de tempo do banco de dados."""
    return _mock_db_time
