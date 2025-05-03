
# Build frontend
FROM node:22-slim@sha256:557e52a0fcb928ee113df7e1fb5d4f60c1341dbda53f55e3d815ca10807efdce AS frontend-builder

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
FROM python:3.13-slim-bookworm@sha256:60248ff36cf701fcb6729c085a879d81e4603f7f507345742dc82d4b38d16784 AS api-builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.7.2@sha256:3b898ca84fbe7628c5adcd836c1de78a0f1ded68344d019af8478d4358417399 /uv /uvx /bin/

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
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock ./scripts/entrypoint.sh /app/
COPY ./migrations /app/migrations
COPY ./scripts /app/scripts

COPY ./app /app/app

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync

COPY --from=frontend-builder /frontend/dist /app/app/frontend/build

RUN chmod +x ./entrypoint.sh

# By default, run the API server
CMD ["./entrypoint.sh"]
