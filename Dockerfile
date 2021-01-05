FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./pyproject.toml ./app/poetry.lock* /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-root --no-dev

COPY ./ /app
