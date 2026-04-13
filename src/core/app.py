"""Core application module for Fast Zero.
This module defines the FastAPI application instance and includes the main
endpoint.
"""

from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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
