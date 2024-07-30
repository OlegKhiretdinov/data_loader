FROM python:3.10 AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="/root/.local/bin:$PATH" \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-dev

FROM python:3.10
WORKDIR /app
COPY --from=builder . /app
COPY . /app
RUN chmod +x ./starter.sh
CMD ./starter.sh
# CMD ["app/.venv/bin/python3", "-m", "flask",  "--app", "app/web_app:app", "run", "--port=5000", "--host=0.0.0.0"]
# CMD ["app/.venv/bin/python3", "-m", "flask",  "--app", "app/file_storage:app", "run", "--port=5001", "--host=0.0.0.0"]
