#!/usr/bin/env bash

set -e
set -x

source .env

SELECT_QUERY="SELECT id, as_of, from_iso_code AS base_currency_code, to_iso_code AS quote_currency_code, rate, created_at, updated_at FROM exchange_rates;"

# Extract from source database
psql "host=$SOURCE_DB_HOST port=$SOURCE_DB_PORT dbname=$SOURCE_DB user=$SOURCE_DB_USER password=$SOURCE_DB_PASSWORD" << EOF
\COPY ($SELECT_QUERY) TO 'tmp/exchange_rates.csv' WITH CSV HEADER;
EOF

# Import to destination database
psql "host=$POSTGRES_USER port=$POSTGRES_PORT dbname=$POSTGRES_DB user=$POSTGRES_USER password=$POSTGRES_PASSWORD" << EOF
\COPY exchange_rates FROM 'tmp/exchange_rates.csv' WITH CSV HEADER;
UPDATE exchange_rates SET source = 'openexchangerates.org' WHERE source IS NULL;
EOF
