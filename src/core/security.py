"""
gerenciar o jwt e a autenticação do usuário.
"""

from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_session
from core.models import User
from core.settings import Settings

settings = Settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
pwd_context = PasswordHash.recommended()

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()


def create_access_token(data: dict):
    """Função para criar um token de acesso JWT."""
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    """Função para gerar um hash de senha."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Função para verificar se a senha fornecida corresponde ao
    hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_schema),
):
    """Função para obter o usuário actual a partir do token de acesso."""
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_email: str = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user
