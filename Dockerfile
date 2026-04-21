FROM python:3.14-slim

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app/src

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev --no-root

COPY . .
RUN chmod +x /app/entrypoint.sh

EXPOSE 8008
CMD ["uvicorn", "core.app:app", "--host", "0.0.0.0", "--port", "8008"]
