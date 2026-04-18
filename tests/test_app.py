"""Testes para a aplicação FastAPI definida em app.py."""

from http import HTTPStatus


def test_root_deve_retornar_hello_world(client):
    """Teste para verificar se o endpoint raiz retorna a mensagem correta."""
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_html_deve_retornar_pagina_html(client):
    """Teste para verificar se o endpoint
    html retorna a página HTML correta."""
    response = client.get('/exercicio-html')
    assert response.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user(client):
    """Teste para verificar se o endpoint de criação de usuário funciona
    corretamente."""

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_red_users(client):
    """Teste para verificar se o endpoint de leitura de usuários retorna a
    lista correta de usuários."""
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    """Teste para verificar se o endpoint de atualização de usuário funciona
    corretamente."""
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    """Teste para verificar se o endpoint de exclusão de usuário funciona
    corretamente."""
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
