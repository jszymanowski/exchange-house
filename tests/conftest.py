from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.database import TORTOISE_ORM
from app.main import app
from tests.utilities.database_helper import DatabaseTestHelper


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_database() -> AsyncGenerator[DatabaseTestHelper]:
    """Initialize Tortoise ORM with the pytest-postgresql database."""
    # Source: https://tortoise.github.io/examples/fastapi.html?h=drop_databases#main-py
    # Perhaps this should be moved to app.main.lifespan

    async with RegisterTortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        _create_db=True,
    ):
        # db connected
        yield DatabaseTestHelper
        # app teardown
    # db connections closed
    await Tortoise._drop_databases()
