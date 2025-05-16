from collections.abc import AsyncGenerator

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from app.core.database import TORTOISE_ORM
from app.core.dependencies import get_exchange_rate_service, get_firebase_service
from app.core.logger import setup_logging
from app.main import app
from app.services.exchange_rate_service import ExchangeRateServiceInterface
from app.services.firebase_service import FirebaseService
from tests.support.database_test_helper import DatabaseTestHelper, get_database_test_helper
from tests.support.mock_exchange_rate_service import MockExchangeRateService
from tests.support.mock_firebase_client import MockFirebaseClient

setup_logging()


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
        yield get_database_test_helper()
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


@pytest.fixture
async def test_firebase_client() -> MockFirebaseClient:
    return MockFirebaseClient()


@pytest.fixture(autouse=True)
async def test_firebase_service(test_firebase_client: MockFirebaseClient) -> AsyncGenerator[FirebaseService]:
    mocked_service = FirebaseService(client=test_firebase_client)
    app.dependency_overrides[get_firebase_service] = lambda: mocked_service
    yield mocked_service
    app.dependency_overrides = {}
