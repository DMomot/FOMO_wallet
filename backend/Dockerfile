# syntax=docker/dockerfile:1.3

# DOCKER_BUILDKIT=1 docker build -t backend .
# docker run --rm --name backend --net=host -v ${PWD}/.secrets.toml:/app/.secrets.toml:ro -ti backend -- uvicorn backend.main:app --port=8000

FROM python:3.11
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -yqq --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "poetry==1.7.0"

WORKDIR /app

COPY poetry.lock    /app
COPY pyproject.toml /app

RUN --mount=type=cache,target=/root/.cache/pypoetry/cache \
    --mount=type=cache,target=/root/.cache/pypoetry/artifacts \
    poetry install --only main

COPY src/backend   /app/src/backend
RUN poetry install

# HEALTHCHECK --interval=1m CMD curl http://localhost:8000/v1/healthcheck

EXPOSE 8000

ENTRYPOINT [ "poetry", "run" ]
CMD [ "uvicorn", "backend.main:app", "--proxy-headers", "--host=0.0.0.0", "--port=8000" ]
