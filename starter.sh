#!/bin/bash

set -m

app/.venv/bin/python3 -m flask --app app/web_app:app run --port=5000 --host=0.0.0.0 &

app/.venv/bin/python3 -m flask --app app/file_storage:app run --port=5001 --host=0.0.0.0

fg %1