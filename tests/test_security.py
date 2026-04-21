"""
testa as funcionalidades de segurança, como autenticação e autorização,
para garantir que os usuários só possam acessar os recursos permitidos.
"""

from http import HTTPStatus

from jwt import decode

from core.security import SECRET_KEY, create_access_token


def test_jwd():
    """Teste para verificar se a função de criação de token JWT funciona
    corretamente."""
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])
    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    """Teste para verificar se a função de decodificação de token JWT
    lança um error quando o token é inválido."""
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalidtoken'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
