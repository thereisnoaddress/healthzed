# syntax = docker/dockerfile:1.2

FROM python:3.9

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1

# System deps:
COPY .env.test /etc/secrets/.env
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

EXPOSE 8000
CMD ["uvicorn", "--reload", "endpoint:app", "--host", "0.0.0.0"]