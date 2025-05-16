from datetime import date
from typing import Any

import pytest
from freezegun import freeze_time
from pytest_mock import MockFixture

from app.models import ExchangeRate
from app.services.firebase_service import FirebaseService
from tests.support.mock_firebase_client import MockFirebaseClient


@freeze_time("2023-01-02 01:23:45")
@pytest.mark.asyncio
async def test_update_exchange_rates_success(test_firebase_client: MockFirebaseClient, mocker: MockFixture) -> None:
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 1)),
    ]

    firebase_set_spy = mocker.spy(test_firebase_client, "set")
    firebase_service = FirebaseService(client=test_firebase_client)
    result = firebase_service.update_exchange_rates(exchange_rates)

    assert result[0] is True
    assert result[1] is None
    assert firebase_set_spy.call_count == 1
    assert firebase_set_spy.call_args[0][0] == (
        {
            "base": "USD",
            "rates": {"EUR": "1.02000000", "JPY": "100.03000000"},
            "date": "2023-01-01",
            "timestamp": "2023-01-02 01:23:45",
        }
    )


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_invalid_exchange_rate_dates(
    test_firebase_client: MockFirebaseClient,
    mocker: MockFixture,
) -> None:
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 2)),
    ]

    firebase_set_spy = mocker.spy(test_firebase_client, "set")
    firebase_service = FirebaseService(client=test_firebase_client)

    with pytest.raises(
        ValueError,
        match=r"As of date \(2023-01-02\) differs from the first rate's as of date \(2023-01-01\)",
    ):
        firebase_service.update_exchange_rates(exchange_rates)

    assert firebase_set_spy.call_count == 0


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_invalid_exchange_rate_base_currency(
    test_firebase_client: MockFirebaseClient,
    mocker: MockFixture,
) -> None:
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="EUR", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 1)),
    ]

    firebase_set_spy = mocker.spy(test_firebase_client, "set")
    firebase_service = FirebaseService(client=test_firebase_client)

    with pytest.raises(
        ValueError,
        match=r"Base currency code \(EUR\) differs from configuration \(USD\)",
    ):
        firebase_service.update_exchange_rates(exchange_rates)

    assert firebase_set_spy.call_count == 0


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_no_exchange_rates(
    test_firebase_client: MockFirebaseClient,
    mocker: MockFixture,
) -> None:
    exchange_rates: list[ExchangeRate] = []

    firebase_set_spy = mocker.spy(test_firebase_client, "set")
    firebase_service = FirebaseService(client=test_firebase_client)

    with pytest.raises(ValueError, match="No exchange rates provided"):
        firebase_service.update_exchange_rates(exchange_rates)

    assert firebase_set_spy.call_count == 0


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_with_multiple_dates(
    test_firebase_client: MockFirebaseClient,
    mocker: MockFixture,
) -> None:
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 2)),
    ]

    firebase_set_spy = mocker.spy(test_firebase_client, "set")
    firebase_service = FirebaseService(client=test_firebase_client)

    with pytest.raises(
        ValueError,
        match=r"As of date \(2023-01-02\) differs from the first rate's as of date \(2023-01-01\)",
    ):
        firebase_service.update_exchange_rates(exchange_rates)

    assert firebase_set_spy.call_count == 0


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_remote_error() -> None:
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 1)),
    ]

    class ErrorFirebaseClient(MockFirebaseClient):
        def set(self, data: dict[str, Any]) -> None:
            raise Exception("Error updating exchange rates")

    firebase_service = FirebaseService(client=ErrorFirebaseClient())

    result = firebase_service.update_exchange_rates(exchange_rates)

    assert result[0] is False
    assert isinstance(result[1], Exception)
    assert str(result[1]) == "Error updating exchange rates"
