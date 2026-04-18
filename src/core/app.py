"""Core application module for Fast Zero.
This module defines the FastAPI application instance and includes the main
endpoint.
"""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from core.schemas import Message, UseDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    """Endpoint to return a simple message."""
    return {'message': 'Hello World'}


@app.get('/exercicio-html', response_class=HTMLResponse)
def exercicio_aula_02():
    """Endpoint to return a simple HTML page."""
    return """
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
    """


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    """Create a new user."""
    use_with_id = UseDB(**user.model_dump(), id=len(database) + 1)
    database.append(use_with_id)
    return use_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    """Endpoint to return a list of all users."""
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    """Endpoint to update an existing user."""
    if user_id > len(database) or user_id < 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UseDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    """Endpoint to delete an existing user."""
    if user_id > len(database) or user_id < 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]
    return {'message': 'User deleted'}
