#!/usr/bin/env bash

set -e
set -x

uv run -m app.pre_start

fastapi run --workers 4 --host 0.0.0.0 --port 8000 app/main.py
