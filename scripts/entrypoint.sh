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
echo "Running migrations..."
uv run aerich upgrade

# Start the application
uv run -m app.start
