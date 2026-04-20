"""Testes para a aplicação FastAPI definida em app.py."""

from http import HTTPStatus

from core.schemas import UserPublic


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


def test_red_users(client, user):
    """Teste para verificar se o endpoint de leitura de usuários retorna a
    lista correta de usuários."""
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_should_return_not_found(client):
    """Teste para verificar se o endpoint de leitura de usuário por ID
    retorna o error correto quando o usuário não existe."""
    response = client.get('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user(client, user):
    """Teste para verificar se o endpoint de leitura de usuário por ID
    retorna o usuário correto."""
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user):
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


def test_update_user_should_return_not_found(client):
    """Teste para verificar se o endpoint de atualização de usuário
    retorna o error correto quando o usuário não existe."""
    response = client.put(
        '/users/999',
        json={
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'anotherpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user):
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    response = client.put(
        '/users/1',
        json={
            'username': 'charlie',
            'email': 'alice@example.com',
            'password': 'anotherpassword',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user):
    """Teste para verificar se o endpoint de exclusão de usuário funciona
    corretamente."""
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_not_found(client):
    """Teste para verificar se o endpoint de exclusão de usuário
    retorna o error correto quando o usuário não existe."""
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users(client):
    """Teste para verificar se o endpoint de leitura de usuários retorna a
    lista correta de usuários após a exclusão."""
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    """Teste para verificar se o endpoint de leitura de usuários retorna a
    lista correta de usuários quando há usuários no banco de dados."""
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}
