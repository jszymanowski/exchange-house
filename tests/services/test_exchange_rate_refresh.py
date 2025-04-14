import json
from datetime import date
from decimal import Decimal
from importlib import resources

import pytest
from pytest_httpx import HTTPXMock

from app.models.exchange_rate import ExchangeRate
from app.services.exchange_rate_refresh import ExchangeRateRefresh
from app.services.exchange_rate_service import ExchangeRateService
from tests.support.database_helper import DatabaseTestHelper


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

    subject = ExchangeRateRefresh(start_date=start_date, end_date=end_date, exchange_rate_service=exchange_rate_service)
    await subject.save()

    forward_rate = await exchange_rate_service.get_latest_rate("GBP", "USD", date(2025, 1, 31))
    inverse_rate = await exchange_rate_service.get_latest_rate("USD", "GBP", date(2025, 1, 31))

    assert forward_rate is not None
    assert inverse_rate is not None

    assert forward_rate.rate == Decimal("1.26231547")
    assert inverse_rate.rate == Decimal("0.79219500")

    record_count = await test_database.count_records(ExchangeRate)
    assert record_count == 1

    assert len(httpx_mock.get_requests()) == 2
