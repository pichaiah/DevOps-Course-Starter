FROM python:3.8-slim-buster as base
WORKDIR /usr/src/app
RUN pip install poetry
ENV PATH=/root/.poetry/bin:${PATH}

FROM base as production
COPY pyproject.toml .
RUN poetry install
COPY ./ ./
ENTRYPOINT poetry run gunicorn "app:create_app()" --bind 0.0.0.0:5000

FROM base as development
COPY ./pyproject.toml ./
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0

