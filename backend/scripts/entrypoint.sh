#!/usr/bin/env bash

set -e
set -x

uv run -m app.pre_start

uv run -m app.start
