#!/usr/bin/env bash

set -e
set -x

# Wait for database to be ready
uv run -m app.pre_start

# Run migrations
aerich upgrade

# Start the application
fastapi run --workers 4 --host 0.0.0.0 --port 8000 app/main.py
