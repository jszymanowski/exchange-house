#!/usr/bin/env bash

set -e
set -x

REPORT_TITLE="Coverage report"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --report-title=*)
      REPORT_TITLE="${1#*=}"
      shift
      ;;
    --report-title)
      REPORT_TITLE="$2"
      shift 2
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

coverage run --source=app -m pytest "${ARGS[@]}"
coverage report --show-missing
coverage html --title "$REPORT_TITLE"
coverage xml
