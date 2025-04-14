from datetime import date
from decimal import Decimal

import pytest
from tortoise import Tortoise, connections
from tortoise.backends.base.client import BaseDBAsyncClient

from app.core.config import settings
from app.core.database import TORTOISE_ORM
from app.models.exchange_rate import ExchangeRate


@pytest.fixture(autouse=True)  # (scope="session")
async def initialize_tests():
    """Initialize Tortoise ORM with the pytest-postgresql database."""

    print(settings.DATABASE_URL)

    await Tortoise.init(TORTOISE_ORM)

    conn: BaseDBAsyncClient = connections.get("default")
    await conn.db_create()

    await Tortoise.generate_schemas()

    yield

    await Tortoise._drop_databases()
    await connections.close_all()


@pytest.mark.asyncio
async def test_exchange_rate_model() -> None:
    exchange_rate = ExchangeRate(
        as_of=date(2021, 1, 1),
        base_currency_code="USD",
        quote_currency_code="EUR",
        rate=Decimal("0.85"),
        data_source="test",
    )

    await exchange_rate.save()

    committed_record = await ExchangeRate.get(id=exchange_rate.id)

    print(committed_record)

    assert committed_record.id is not None
    assert committed_record.as_of == date(2021, 1, 1)
    assert committed_record.base_currency_code == "USD"
    assert committed_record.quote_currency_code == "EUR"
    assert committed_record.rate == Decimal("0.85")
    assert committed_record.data_source == "test"
