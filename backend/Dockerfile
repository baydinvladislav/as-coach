FROM python:3.10

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2 \
  DATABASE_URL=postgresql://postgres:postgres@0.0.0.0:5432/as_coach

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

ENTRYPOINT alembic upgrade head
ENTRYPOINT uvicorn src.main:app --host 0.0.0.0 --port 8000
