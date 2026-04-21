"""Conftest.py - Configurações e fixtures para os testes.
Este arquivo é utilizado para definir fixtures e configurações comuns
para os testes, como a criação de um client de teste do FastAPI.
"""

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from core.database import get_session
from core.security import get_password_hash
from src.core.app import app
from src.core.models import User, table_registry


@pytest.fixture
def client(session):
    """Fixture para criar um client de teste do FastAPI."""

    def get_session_override():
        return session

    with TestClient(app) as client_app:
        app.dependency_overrides[get_session] = get_session_override
        yield client_app

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """Fixture para criar uma sessão de banco de dados para os testes."""
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
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


@pytest.fixture
def user(session):
    """Fixture para criar um usuário de teste."""
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@example.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    """Fixture para obter um token de
    acesso JWT para o usuário de teste."""
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    print(response.json())
    return response.json()['access_token']
