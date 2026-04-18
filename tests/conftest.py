"""Conftest.py - Configurações e fixtures para os testes.
Este arquivo é utilizado para definir fixtures e configurações comuns
para os testes, como a criação de um client de teste do FastAPI.
"""

import pytest
from fastapi.testclient import TestClient

from src.core.app import app


@pytest.fixture
def client():
    """Fixture para criar um client de teste do FastAPI."""
    with TestClient(app) as client_app:
        yield client_app
