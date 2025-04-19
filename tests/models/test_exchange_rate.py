from datetime import date
from decimal import Decimal

import pytest

from app.models.exchange_rate import ExchangeRate
from tests.support.database_test_helper import DatabaseTestHelper


@pytest.mark.asyncio
async def test_exchange_rate_model(test_database: DatabaseTestHelper) -> None:
    exchange_rate = ExchangeRate(
        as_of=date(2021, 1, 1),
        base_currency_code="USD",
        quote_currency_code="EUR",
        rate=Decimal("0.85"),
        data_source="test",
    )

    await exchange_rate.save()

    record_count = await test_database.count_records(ExchangeRate)
    assert record_count == 1

    committed_record = await ExchangeRate.get(id=exchange_rate.id)

    assert committed_record.id is not None
    assert committed_record.as_of == date(2021, 1, 1)
    assert committed_record.base_currency_code == "USD"
    assert committed_record.quote_currency_code == "EUR"
    assert committed_record.rate == Decimal("0.85")
    assert committed_record.data_source == "test"


@pytest.mark.asyncio
async def test_exchange_rate_model_another(test_database: DatabaseTestHelper) -> None:
    exchange_rate = ExchangeRate(
        as_of=date(2021, 1, 1),
        base_currency_code="USD",
        quote_currency_code="EUR",
        rate=Decimal("0.85"),
        data_source="test",
    )

    await exchange_rate.save()

    record_count = await test_database.count_records(ExchangeRate)
    assert record_count == 1

    committed_record = await ExchangeRate.get(id=exchange_rate.id)

    assert committed_record.id is not None
    assert committed_record.as_of == date(2021, 1, 1)
    assert committed_record.base_currency_code == "USD"
    assert committed_record.quote_currency_code == "EUR"
    assert committed_record.rate == Decimal("0.85")
    assert committed_record.data_source == "test"
