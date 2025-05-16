
# Build frontend
FROM node:22-slim@sha256:ec318fe0dc46b56bcc1ca42a202738aeb4f3e347a7b4dd9f9f1df12ea7aa385a AS frontend-builder

WORKDIR /frontend

RUN corepack enable && \
  corepack prepare pnpm@10.8.1 --activate

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

ENV VITE_API_URL="http://exchangehouse.home"
COPY frontend ./
RUN pnpm build

# ----------------------------

# Build backend
FROM python:3.13-slim-bookworm@sha256:914bf5c12ea40a97a78b2bff97fbdb766cc36ec903bfb4358faf2b74d73b555b AS api-builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.4@sha256:9618e472e7ed9aa980719c68e51416e7ec23d85742d9ccca5c817d76ed2eb5aa /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=backend/uv.lock,target=uv.lock \
  --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./backend/pyproject.toml ./backend/uv.lock ./backend/scripts/entrypoint.sh /app/
COPY ./backend/migrations /app/migrations
COPY ./backend/scripts /app/scripts

COPY ./backend/app /app/app

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync

COPY --from=frontend-builder /frontend/dist /app/app/frontend/build

RUN chmod +x ./entrypoint.sh

# By default, run the API server
CMD ["./entrypoint.sh"]
