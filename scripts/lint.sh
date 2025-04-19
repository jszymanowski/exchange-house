#!/usr/bin/env bash

set -e
set -x


# Check for --apply-fixes flag
APPLY_FIXES=false
for arg in "$@"; do
  if [ "$arg" == "--apply-fixes" ]; then
    APPLY_FIXES=true
  fi
done

mypy app # TODO: add tests

if [ "$APPLY_FIXES" = true ]; then
  ruff check --fix app tests
  ruff format app tests
else
  ruff check app tests
  ruff format app tests --check
fi
