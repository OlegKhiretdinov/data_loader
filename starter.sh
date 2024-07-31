#!/bin/bash

set -m

.venv/bin/python3 -m gunicorn -w 5 -b 0.0.0.0:5000 web_app:app &

.venv/bin/python3 -m gunicorn -w 5 -b 0.0.0.0:5001 file_storage:app

fg %1