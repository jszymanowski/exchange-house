#!/usr/bin/env bash

set -e
set -x

# Check if required environment variables are set
if [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ] || [ -z "$POSTGRES_DB" ]; then
    echo "ERROR: POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB environment variables must be set"
    exit 1
fi

# Wait for database to be ready
uv run -m app.pre_start

# Initialize database, or run migrations if already initialized
if aerich migrate --dry-run 2>&1 | grep -q "You need to run \`aerich init-db\`"; then
  echo "First-time setup: Initializing Aerich..."
  aerich init -t app.core.database.TORTOISE_ORM
  aerich init-db
else
  echo "Running migrations..."
  aerich upgrade
fi

# Start the application
fastapi run --workers 4 --host 0.0.0.0 --port 8000 app/main.py
