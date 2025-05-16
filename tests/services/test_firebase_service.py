from datetime import date

import pytest
from freezegun import freeze_time
from pytest_mock import MockFixture, MockType

from app.models import ExchangeRate
from app.services.firebase_service import FirebaseService


class MockFirebaseClient:
    def __init__(self):
        pass

    def collection(self, collection_name: str):
        return self

    def document(self, document_name: str):
        return self

    def set(self, data: dict):
        pass


@pytest.fixture
def mock_firebase(mocker: MockFixture) -> tuple[MockFirebaseClient, MockType]:
    mock_client = MockFirebaseClient()
    return [mock_client, mocker.spy(mock_client, "set")]


@freeze_time("2023-01-02 01:23:45")
@pytest.mark.asyncio
async def test_update_exchange_rates_success(mock_firebase: tuple[MockFirebaseClient, MockType]):
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 1)),
    ]

    [mock_client, firebase_set_spy] = mock_firebase

    firebase_service = FirebaseService(client=mock_client)
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
    mock_firebase: tuple[MockFirebaseClient, MockType],
):
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 2)),
    ]

    [mock_client, firebase_set_spy] = mock_firebase

    firebase_service = FirebaseService(client=mock_client)

    with pytest.raises(
        ValueError,
        match=r"As of date \(2023-01-02\) differs from the first rate's as of date \(2023-01-01\)",
    ):
        firebase_service.update_exchange_rates(exchange_rates)


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_invalid_exchange_rate_base_currency(
    mock_firebase: tuple[MockFirebaseClient, MockType],
):
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="EUR", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 1)),
    ]

    [mock_client, firebase_set_spy] = mock_firebase

    firebase_service = FirebaseService(client=mock_client)

    with pytest.raises(
        ValueError,
        match=r"Base currency code \(EUR\) differs from configuration \(USD\)",
    ):
        firebase_service.update_exchange_rates(exchange_rates)


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_no_exchange_rates(
    mock_firebase: tuple[MockFirebaseClient, MockType],
):
    exchange_rates = []

    [mock_client, firebase_set_spy] = mock_firebase

    firebase_service = FirebaseService(client=mock_client)

    with pytest.raises(ValueError, match="No exchange rates provided"):
        firebase_service.update_exchange_rates(exchange_rates)


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_with_multiple_dates(
    mock_firebase: tuple[MockFirebaseClient, MockType],
):
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 2)),
    ]

    [mock_client, firebase_set_spy] = mock_firebase

    firebase_service = FirebaseService(client=mock_client)

    with pytest.raises(
        ValueError,
        match=r"As of date \(2023-01-02\) differs from the first rate's as of date \(2023-01-01\)",
    ):
        firebase_service.update_exchange_rates(exchange_rates)


@pytest.mark.asyncio
async def test_update_exchange_rates_failure_remote():
    exchange_rates = [
        ExchangeRate(base_currency_code="USD", quote_currency_code="EUR", rate=1.02, as_of=date(2023, 1, 1)),
        ExchangeRate(base_currency_code="USD", quote_currency_code="JPY", rate=100.03, as_of=date(2023, 1, 1)),
    ]

    class ErrorFirebaseClient(MockFirebaseClient):
        def set(self, data: dict):
            raise Exception("Error updating exchange rates")

    firebase_service = FirebaseService(client=ErrorFirebaseClient())

    result = firebase_service.update_exchange_rates(exchange_rates)

    assert result[0] is False
    assert isinstance(result[1], Exception)
    assert str(result[1]) == "Error updating exchange rates"
