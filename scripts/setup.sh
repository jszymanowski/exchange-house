#!/usr/bin/env bash

set -e

if [ "$1" == "--debug" ]; then
  set -x
fi

POSTGRES_DB=${POSTGRES_DB:-"exchange_house_development"}
POSTGRES_USER=${POSTGRES_USER:-"postgres"}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-"postgres"}

create_db_if_not_exists() {
  local db_name=$1
  echo "Checking if database $db_name exists..."

  # Check if database exists
  if psql -U "$POSTGRES_USER" -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
    echo "Database $db_name already exists. Skipping creation."
  else
    echo "Database $db_name does not exist. Creating it now..."
    psql -U "$POSTGRES_USER" -c "CREATE DATABASE \"$db_name\";"
    echo "Database $db_name created successfully."
  fi
}

# Create the main database
echo "Creating database $POSTGRES_DB"
create_db_if_not_exists "$POSTGRES_DB"

echo "Syncing dependencies"
uv sync --frozen --no-install-project

echo "Running pre-start"
uv run -m app.pre_start

echo "Setup complete. Next steps:

1. Run 'bin/seed' to seed the database with data.
2. Run 'bin/dev' to start the server.
3. Run 'bin/test' to run the tests.

"
