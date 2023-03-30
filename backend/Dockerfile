FROM python:3.10

# Сборка зависимостей
ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.3.2 POETRY_HOME=/root/poetry python3 -

ENV PATH="${PATH}:/root/poetry/bin"
ENV PYTHONPATH "${PYTHONPATH}:/backend"

WORKDIR /code

ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--port", "8000"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Установка питонячьих библиотек
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копирование в контейнер папок и файлов.
COPY . /code
COPY ./docker-entrypoint.sh /code
RUN chmod u+x ./docker-entrypoint.sh
