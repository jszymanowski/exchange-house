from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.database import TORTOISE_ORM
from app.core.dependencies import get_exchange_rate_service
from app.main import app
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from tests.support.database_helper import DatabaseTestHelper
from tests.support.mock_exchange_rate_service import MockExchangeRateService


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_database() -> AsyncGenerator[DatabaseTestHelper]:
    """Initialize Tortoise ORM with the pytest-postgresql database."""

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


@pytest.fixture
async def test_exchange_rate_service() -> ExchangeRateServiceInterface:
    return MockExchangeRateService()


@pytest.fixture
async def with_test_exchange_rate_service(
    test_exchange_rate_service: ExchangeRateServiceInterface,
) -> AsyncGenerator[ExchangeRateServiceInterface]:
    app.dependency_overrides[get_exchange_rate_service] = lambda: test_exchange_rate_service
    yield test_exchange_rate_service
    app.dependency_overrides = {}
