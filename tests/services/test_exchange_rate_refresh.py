import json
from datetime import date
from decimal import Decimal
from importlib import resources

import pytest
from pytest_httpx import HTTPXMock

from app.models import Currency
from app.models.exchange_rate import ExchangeRate
from app.services.exchange_rate_refresh import ExchangeRateRefresh
from app.services.exchange_rate_service import ExchangeRateService
from tests.support.database_test_helper import DatabaseTestHelper


@pytest.mark.asyncio
async def test_exchange_rate_refresh(httpx_mock: HTTPXMock, test_database: DatabaseTestHelper) -> None:
    start_date = date(2025, 1, 31)
    end_date = date(2025, 2, 1)

    fixture_data = json.loads(
        resources.files("tests.support.open_exchange_rates").joinpath("historical.json").read_text()
    )
    httpx_mock.add_response(
        method="GET",
        url="https://openexchangerates.org/api/historical/2025-01-31.json?app_id=FAKE_OER_APP_ID",
        json=fixture_data,
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url="https://openexchangerates.org/api/historical/2025-02-01.json?app_id=FAKE_OER_APP_ID",
        json=fixture_data,
        status_code=200,
    )

    exchange_rate_service = ExchangeRateService()

    record_count = await test_database.count_records(ExchangeRate)
    assert record_count == 0
    subject = ExchangeRateRefresh(start_date=start_date, end_date=end_date, exchange_rate_service=exchange_rate_service)
    result = await subject.save()
    assert result

    forward_rate = await exchange_rate_service.get_latest_rate(Currency("GBP"), Currency("USD"), date(2025, 1, 31))
    inverse_rate = await exchange_rate_service.get_latest_rate(Currency("USD"), Currency("GBP"), date(2025, 1, 31))
    unsupported_rate = await exchange_rate_service.get_latest_rate(Currency("BTC"), Currency("USD"), date(2025, 1, 31))

    assert forward_rate is not None
    assert inverse_rate is not None
    assert unsupported_rate is not None

    assert forward_rate.rate == Decimal("1.26231547")
    assert inverse_rate.rate == Decimal("0.79219500")
    assert unsupported_rate.rate == Decimal("44959.60559276")

    # 672 records = 168 unique currencies * 2 rates (forward and inverse) * 2 days (1/31 and 2/1)
    # Note: fixture data has 169 currencies.  USD is ignored (not written to DB).
    record_count = await test_database.count_records(ExchangeRate)
    assert record_count == 672

    assert len(httpx_mock.get_requests()) == 2


@pytest.mark.asyncio
async def test_exchange_rate_refresh_handles_api_error(
    httpx_mock: HTTPXMock, test_database: DatabaseTestHelper
) -> None:
    start_date = date(2025, 1, 31)
    end_date = date(2025, 1, 31)

    # Mock API error response
    error_response = {"error": True, "status": 400, "message": "not_available", "description": "Invalid API key"}
    httpx_mock.add_response(
        method="GET",
        url="https://openexchangerates.org/api/historical/2025-01-31.json?app_id=FAKE_OER_APP_ID",
        json=error_response,
        status_code=400,
    )

    exchange_rate_service = ExchangeRateService()
    subject = ExchangeRateRefresh(start_date=start_date, end_date=end_date, exchange_rate_service=exchange_rate_service)

    # Verify that the error is properly propagated
    with pytest.raises(Exception) as excinfo:
        await subject.save()

    assert "Invalid API key" in str(excinfo.value)

    # Verify no records were created
    record_count = await test_database.count_records(ExchangeRate)
    assert record_count == 0
