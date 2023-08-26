FROM python:3.11-slim

ENV PYTHONPATH=/bot/

RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false

WORKDIR /bot

COPY ./pyproject.toml ./poetry.lock /bot/


RUN poetry export -f requirements.txt --output /bot/requirements.txt \
    --without-hashes --without-urls \
    && pip install -r /bot/requirements.txt

COPY ./src/ /bot/src
