from datetime import date
from decimal import Decimal
from typing import Literal

import pytest

from app.models.currency_pair import CurrencyPair
from app.models.exchange_rate import ExchangeRate
from app.services.exchange_rate_service import ExchangeRateService
from tests.support.database_test_helper import DatabaseTestHelper
from tests.support.decimal import quantize_decimal
from tests.support.factories import build_exchange_rate_pair


@pytest.fixture(autouse=True)
async def exchange_rates(test_database: DatabaseTestHelper) -> list[ExchangeRate]:
    exchange_rates = [
        *build_exchange_rate_pair(
            base_currency_code="USD", quote_currency_code="EUR", as_of=date(2023, 1, 1), rate=Decimal("0.85")
        ),
        *build_exchange_rate_pair(
            base_currency_code="USD", quote_currency_code="JPY", as_of=date(2023, 1, 1), rate=Decimal("100")
        ),
        *build_exchange_rate_pair(
            base_currency_code="USD", quote_currency_code="EUR", as_of=date(2023, 1, 20), rate=Decimal("0.87")
        ),
        *build_exchange_rate_pair(
            base_currency_code="USD", quote_currency_code="JPY", as_of=date(2023, 1, 20), rate=Decimal("102")
        ),
        *build_exchange_rate_pair(
            base_currency_code="USD", quote_currency_code="JPY", as_of=date(2023, 1, 15), rate=Decimal("101")
        ),
        # Invalid currencies
        *build_exchange_rate_pair(
            base_currency_code="BTC", quote_currency_code="USD", as_of=date(2023, 1, 15), rate=Decimal("0.00002")
        ),
    ]
    await ExchangeRate.bulk_create(exchange_rates)

    return exchange_rates


@pytest.mark.asyncio
async def test_get_available_dates() -> None:
    service = ExchangeRateService()
    results = await service.get_available_dates()

    assert len(results) == 3
    assert results[0] == date(2023, 1, 1)
    assert results[1] == date(2023, 1, 15)
    assert results[2] == date(2023, 1, 20)


@pytest.mark.asyncio
async def test_get_currency_pairs() -> None:
    service = ExchangeRateService()
    results = await service.get_currency_pairs()

    assert results == [
        CurrencyPair(base_currency_code="EUR", quote_currency_code="USD"),
        CurrencyPair(base_currency_code="JPY", quote_currency_code="USD"),
        CurrencyPair(base_currency_code="USD", quote_currency_code="EUR"),
        CurrencyPair(base_currency_code="USD", quote_currency_code="JPY"),
    ]


@pytest.mark.asyncio
async def test_get_latest_rate_success() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    expected_rate = Decimal("0.87")

    service = ExchangeRateService()
    result = await service.get_latest_rate(base_currency_code, quote_currency_code)

    assert result is not None
    assert result.base_currency_code == base_currency_code
    assert result.quote_currency_code == quote_currency_code
    assert quantize_decimal(result.rate) == quantize_decimal(expected_rate)
    assert result.as_of == date(2023, 1, 20)


@pytest.mark.asyncio
async def test_get_latest_rate_success_with_as_of() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    as_of = date(2023, 1, 1)
    expected_rate = Decimal("0.85")

    service = ExchangeRateService()
    result = await service.get_latest_rate(base_currency_code, quote_currency_code, as_of)

    assert result is not None
    assert result.base_currency_code == base_currency_code
    assert result.quote_currency_code == quote_currency_code
    assert quantize_decimal(result.rate) == quantize_decimal(expected_rate)
    assert result.as_of == as_of


@pytest.mark.asyncio
async def test_get_latest_rate_success_same_currency() -> None:
    base_currency_code = "EUR"
    quote_currency_code = "EUR"
    as_of = date(2023, 1, 1)
    expected_rate = Decimal("1")

    service = ExchangeRateService()
    result = await service.get_latest_rate(base_currency_code, quote_currency_code, as_of)

    assert result is not None
    assert result.base_currency_code == base_currency_code
    assert result.quote_currency_code == quote_currency_code
    assert quantize_decimal(result.rate) == quantize_decimal(expected_rate)
    assert result.as_of == as_of


@pytest.mark.asyncio
async def test_get_latest_rate_not_found() -> None:
    base_currency_code = "USD"
    quote_currency_code = "XYZ"
    as_of = date(2023, 1, 1)

    service = ExchangeRateService()
    result = await service.get_latest_rate(base_currency_code, quote_currency_code, as_of)

    assert result is None


@pytest.mark.asyncio
async def test_get_historical_rates_success() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    start_date = date(2023, 1, 1)

    service = ExchangeRateService()
    results = await service.get_historical_rates(
        base_currency_code=base_currency_code, quote_currency_code=quote_currency_code, start_date=start_date
    )

    assert len(results) == 2
    assert quantize_decimal(results[0].rate) == quantize_decimal("0.85")
    assert results[0].as_of == date(2023, 1, 1)

    assert quantize_decimal(results[1].rate) == quantize_decimal("0.87")
    assert results[1].as_of == date(2023, 1, 20)


@pytest.mark.asyncio
async def test_get_historical_rates_not_found() -> None:
    base_currency_code = "USD"
    quote_currency_code = "XYZ"
    start_date = date(2023, 1, 1)

    service = ExchangeRateService()
    results = await service.get_historical_rates(
        base_currency_code=base_currency_code, quote_currency_code=quote_currency_code, start_date=start_date
    )

    assert results == []


@pytest.mark.asyncio
async def test_get_historical_rates_with_limit() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    start_date = date(2023, 1, 1)
    limit = 1

    service = ExchangeRateService()
    results = await service.get_historical_rates(
        base_currency_code=base_currency_code,
        quote_currency_code=quote_currency_code,
        start_date=start_date,
        limit=limit,
    )

    assert len(results) == 1
    assert quantize_decimal(results[0].rate) == quantize_decimal("0.85")
    assert results[0].as_of == date(2023, 1, 1)


@pytest.mark.asyncio
async def test_get_historical_rates_with_sort_order_desc() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    start_date = date(2023, 1, 1)
    sort_order: Literal["desc", "asc"] = "desc"

    service = ExchangeRateService()
    results = await service.get_historical_rates(
        base_currency_code=base_currency_code,
        quote_currency_code=quote_currency_code,
        start_date=start_date,
        sort_order=sort_order,
    )

    assert len(results) == 2
    assert results[0].as_of > results[1].as_of


@pytest.mark.asyncio
async def test_create_rate_success() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    as_of = date(2023, 1, 30)
    rate = Decimal("0.90")
    source = "test"

    service = ExchangeRateService()
    result = await service.create_rate(as_of, base_currency_code, quote_currency_code, rate, source)

    assert len(result) == 2
    assert result[0].id is not None
    assert result[0].base_currency_code == base_currency_code
    assert result[0].quote_currency_code == quote_currency_code
    assert quantize_decimal(result[0].rate) == quantize_decimal(rate)
    assert result[0].as_of == as_of
    assert result[0].data_source == source

    assert result[1].id is not None
    assert result[1].base_currency_code == quote_currency_code
    assert result[1].quote_currency_code == base_currency_code
    assert quantize_decimal(result[1].rate) == quantize_decimal(1 / rate)
    assert result[1].as_of == as_of
    assert result[1].data_source == source


@pytest.mark.asyncio
async def test_create_rate_failure() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    as_of = date(2023, 1, 1)
    rate = Decimal("0.85")
    source = "test"

    service = ExchangeRateService()

    with pytest.raises(ValueError) as err:
        await service.create_rate(as_of, base_currency_code, quote_currency_code, rate, source)

    expected_message = f"Failed to create exchange rate for {base_currency_code} to {quote_currency_code} on {as_of}"
    assert expected_message in str(err.value)
