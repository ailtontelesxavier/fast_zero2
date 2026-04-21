"""Conftest.py - Configurações e fixtures para os testes.
Este arquivo é utilizado para definir fixtures e configurações comuns
para os testes, como a criação de um client de teste do FastAPI.
"""

from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from core.app import app
from core.database import get_session
from core.models import User, table_registry
from core.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest_asyncio.fixture
async def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        engine = create_async_engine(
            postgres.get_connection_url().replace(
                'postgresql+psycopg://',
                'postgresql+psycopg_async://',
                1,
            )
        )
        try:
            yield engine
        finally:
            await engine.dispose()


@pytest_asyncio.fixture
async def db_schema(engine):
    """Fixture para criar e destruir o esquema do banco
    de dados para os testes."""
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def session(engine, db_schema):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(engine, db_schema):
    async def get_session_override():
        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session

    client = TestClient(app)
    app.dependency_overrides[get_session] = get_session_override
    yield client

    app.dependency_overrides.clear()
    client.close()


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
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

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
