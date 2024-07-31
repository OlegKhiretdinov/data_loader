FROM python:3.10 AS builder
WORKDIR /app
COPY . ./
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="/root/.local/bin:$PATH" \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-dev

RUN chmod +x ./starter.sh
CMD ./starter.sh
