from http import HTTPStatus

from fastapi.testclient import TestClient

from src.core.app import app


def test_root_deve_retornar_hello_world():
    """Teste para verificar se o endpoint raiz retorna a mensagem correta."""
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_html_deve_retornar_pagina_html():
    """Teste para verificar se o endpoint
    html retorna a página HTML correta."""
    client = TestClient(app)
    response = client.get('/exercicio-html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user():
    """Teste para verificar se o endpoint de criação de usuário funciona
    corretamente."""
    client = TestClient(app)

    response = client.post('/users/', json={
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
