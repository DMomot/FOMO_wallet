# syntax=docker/dockerfile:1.6

# DOCKER_BUILDKIT=1 docker image build --tag backend .
# docker run --rm --name backend -v ${PWD}/.env:/app/.env:ro -ti backend

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
# CMD [ "gunicorn", "backend.main:app", "--workers", "3", "--enable-stdio-inheritance", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]
