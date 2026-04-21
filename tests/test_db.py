from dataclasses import asdict

import pytest
from sqlalchemy import select

from core.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    """Teste para verificar se a criação de
    usuário funciona corretamente."""
    with mock_db_time(model=User) as time:
        new_user = User(
            username='bob',
            password='mynewpassword',
            email='bob@example.com',
        )
        session.add(new_user)
        await session.commit()

        user = await session.scalar(select(User).where(User.username == 'bob'))
        assert asdict(user) == {
            'id': 1,
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
            'created_at': time,
            'updated_at': time,
            'todos': [],
        }
