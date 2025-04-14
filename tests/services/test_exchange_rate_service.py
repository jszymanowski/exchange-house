from datetime import date
from decimal import Decimal
from typing import Literal

import pytest
from fastapi import HTTPException

from app.models.currency_pair import CurrencyPair
from app.models.exchange_rate import ExchangeRate
from app.models.exchange_rate_service import ExchangeRateService
from tests.support.database_helper import DatabaseTestHelper
from tests.support.decimal import quantize_decimal
from tests.support.factories import build_exchange_rate


@pytest.fixture(autouse=True)
async def exchange_rates(test_database: DatabaseTestHelper) -> list[ExchangeRate]:
    exchange_rates = [
        *build_exchange_rate(
            base_currency_code="USD", quote_currency_code="EUR", as_of=date(2023, 1, 1), rate=Decimal("0.85")
        ),
        *build_exchange_rate(
            base_currency_code="USD", quote_currency_code="JPY", as_of=date(2023, 1, 2), rate=Decimal("100")
        ),
    ]
    await ExchangeRate.bulk_create(exchange_rates)
    await test_database.done()

    return exchange_rates


@pytest.mark.asyncio
async def test_get_available_dates() -> None:
    service = ExchangeRateService()
    results = await service.get_available_dates()

    assert len(results) == 2
    assert results[0] == date(2023, 1, 1)
    assert results[1] == date(2023, 1, 2)


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


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_latest_rate_success() -> None:
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
    assert result.date == as_of


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_latest_rate_success_custom_from_currency() -> None:
    base_currency_code = "CUSTOM_CAPITAL_ONE"
    quote_currency_code = "USD"
    as_of = date(2023, 1, 1)
    expected_rate = Decimal("0.005")

    service = ExchangeRateService()
    result = await service.get_latest_rate(base_currency_code, quote_currency_code, as_of)

    assert result is not None
    assert result.base_currency_code == base_currency_code
    assert result.quote_currency_code == quote_currency_code
    assert quantize_decimal(result.rate) == quantize_decimal(expected_rate)
    assert result.date == as_of


@pytest.mark.skip(reason="Not yet implemented")
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
    assert result.date == as_of


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_latest_rate_success_custom_to_currency() -> None:
    base_currency_code = "USD"
    quote_currency_code = "CUSTOM_AMEX"
    as_of = date(2023, 1, 1)
    expected_rate = Decimal("166.66666667")

    service = ExchangeRateService()
    result = await service.get_latest_rate(base_currency_code, quote_currency_code, as_of)

    assert result is not None
    assert result.base_currency_code == base_currency_code
    assert result.quote_currency_code == quote_currency_code
    assert quantize_decimal(result.rate) == quantize_decimal(expected_rate)
    assert result.date == as_of


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_latest_rate_not_found() -> None:
    base_currency_code = "USD"
    quote_currency_code = "XYZ"
    as_of = date(2023, 1, 1)

    service = ExchangeRateService()

    with pytest.raises(HTTPException) as excinfo:
        await service.get_latest_rate(base_currency_code, quote_currency_code, as_of)

    assert excinfo.value.status_code == 404
    assert f"No exchange rates found for {base_currency_code} to {quote_currency_code}" in excinfo.value.detail


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_historical_rates_success() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    start_date = date(2023, 1, 1)

    service = ExchangeRateService()
    results = await service.get_historical_rates(base_currency_code, quote_currency_code, start_date)

    assert len(results) == 2
    assert quantize_decimal(results[0].rate) == quantize_decimal("0.85")
    assert results[0].date == date(2023, 1, 1)

    assert quantize_decimal(results[1].rate) == quantize_decimal("0.86")
    assert results[1].date == date(2023, 1, 2)


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_historical_rates_not_found() -> None:
    base_currency_code = "USD"
    quote_currency_code = "XYZ"
    start_date = date(2023, 1, 1)

    service = ExchangeRateService()

    with pytest.raises(HTTPException) as excinfo:
        await service.get_historical_rates(base_currency_code, quote_currency_code, start_date)

    assert excinfo.value.status_code == 404
    assert f"No exchange rates found for {base_currency_code}" in excinfo.value.detail


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_historical_rates_with_limit() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    start_date = date(2023, 1, 1)
    limit = 1

    service = ExchangeRateService()
    results = await service.get_historical_rates(base_currency_code, quote_currency_code, start_date, limit)

    assert len(results) == 1
    assert quantize_decimal(results[0].rate) == quantize_decimal("0.85")
    assert results[0].date == date(2023, 1, 1)


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_get_historical_rates_with_sort_order_desc() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    start_date = date(2023, 1, 1)
    sort_order: Literal["desc", "asc"] = "desc"

    service = ExchangeRateService()
    results = await service.get_historical_rates(
        base_currency_code, quote_currency_code, start_date, sort_order=sort_order
    )

    assert len(results) == 2
    assert results[0].date > results[1].date


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_create_rate_success() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    as_of = date(2023, 1, 1)
    rate = Decimal("0.85")

    service = ExchangeRateService()
    result = await service.create_rate(as_of, base_currency_code, quote_currency_code, rate)

    assert len(result) == 2
    assert result[0].base_currency_code == base_currency_code
    assert result[0].quote_currency_code == quote_currency_code
    assert quantize_decimal(result[0].rate) == quantize_decimal(rate)
    assert result[0].date == as_of

    assert result[1].base_currency_code == quote_currency_code
    assert result[1].quote_currency_code == base_currency_code
    assert quantize_decimal(result[1].rate) == quantize_decimal(1 / rate)
    assert result[1].date == as_of


@pytest.mark.skip(reason="Not yet implemented")
@pytest.mark.asyncio
async def test_create_rate_failure() -> None:
    base_currency_code = "USD"
    quote_currency_code = "EUR"
    as_of = date(2023, 1, 1)
    rate = Decimal("0.85")

    service = ExchangeRateService()

    with pytest.raises(HTTPException) as excinfo:
        await service.create_rate(as_of, base_currency_code, quote_currency_code, rate)

    assert excinfo.value.status_code == 400
    assert (
        f"Failed to create exchange rate for {base_currency_code} to {quote_currency_code} on {as_of}"
        in excinfo.value.detail
    )
