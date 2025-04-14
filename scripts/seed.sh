#!/usr/bin/env bash

set -e
set -x

source .env

# Check for --clear-existing flag
CLEAR_EXISTING=false
for arg in "$@"; do
  if [ "$arg" == "--clear-existing" ]; then
    CLEAR_EXISTING=true
  fi
done

SELECT_QUERY="SELECT id, as_of, from_iso_code AS base_currency_code, to_iso_code AS quote_currency_code, rate, 'openexchangerates.org' AS data_source, created_at, updated_at FROM exchange_rates WHERE from_iso_code NOT LIKE 'CUSTOM%' AND to_iso_code NOT LIKE 'CUSTOM%'"

# Extract from source database
psql "host=$SOURCE_DB_HOST port=$SOURCE_DB_PORT dbname=$SOURCE_DB user=$SOURCE_DB_USER password=$SOURCE_DB_PASSWORD" << EOF
\COPY ($SELECT_QUERY) TO 'tmp/exchange_rates.csv' WITH CSV HEADER;
EOF

# Import to destination database
psql "host=$POSTGRES_HOST port=$POSTGRES_PORT dbname=$POSTGRES_DB user=$POSTGRES_USER password=$POSTGRES_PASSWORD" << EOF
$(if [ "$CLEAR_EXISTING" = true ]; then echo "TRUNCATE TABLE exchange_rates;"; fi)
\COPY exchange_rates(id, as_of, base_currency_code, quote_currency_code, rate, data_source, created_at, updated_at) FROM 'tmp/exchange_rates.csv' WITH CSV HEADER;
EOF
