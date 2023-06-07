FROM python:3.11-slim

# Install curl and nc
RUN apt-get update; apt-get install -y curl; apt-get install -y netcat

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /web/

WORKDIR /web

RUN poetry install --no-root --no-dev

COPY . /web
