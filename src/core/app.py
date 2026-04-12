"""Core application module for Fast Zero.
This module defines the FastAPI application instance and includes the main
endpoint.
"""

from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    """Endpoint to return a simple message."""
    return {'message': 'Hello World'}
