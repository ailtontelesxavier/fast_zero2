"""Conftest.py - Configurações e fixtures para os testes.
Este arquivo é utilizado para definir fixtures e configurações comuns
para os testes, como a criação de um client de teste do FastAPI.
"""

from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.database import get_session
from core.security import get_password_hash
from src.core.app import app
from src.core.models import User, table_registry


@pytest.fixture
def database_url(tmp_path):
    """Fixture para criar uma URL de banco de dados para os testes."""
    return f'sqlite:///{tmp_path / "test.db"}'


@pytest.fixture
def client(database_url):
    """Fixture para criar um client de teste do FastAPI."""
    sync_engine = create_engine(database_url)
    table_registry.metadata.create_all(sync_engine)
    async_engine = create_async_engine(
        database_url.replace('sqlite:///', 'sqlite+aiosqlite:///', 1)
    )

    async def get_session_override():
        async with AsyncSession(
            async_engine, expire_on_commit=False
        ) as session:
            yield session

    client_app = TestClient(app)
    app.dependency_overrides[get_session] = get_session_override
    yield client_app

    app.dependency_overrides.clear()
    client_app.close()
    sync_engine.dispose()


@pytest_asyncio.fixture
async def session(database_url):
    """Fixture para criar uma sessão de banco de dados para os testes."""
    sync_engine = create_engine(database_url)
    table_registry.metadata.create_all(sync_engine)
    async_engine = create_async_engine(
        database_url.replace('sqlite:///', 'sqlite+aiosqlite:///', 1)
    )

    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session

    await async_engine.dispose()
    sync_engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    """Context manager para mockar o tempo do
    banco de dados durante os testes."""

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    """Fixture para fornecer o context manager
    de mock de tempo do banco de dados."""
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    """Fixture para criar um usuário de teste."""
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@example.com',
        password=get_password_hash(password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def token(client, user):
    """Fixture para obter um token de
    acesso JWT para o usuário de teste."""
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    print(response.json())
    return response.json()['access_token']
