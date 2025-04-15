from datetime import date
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.services.exchange_rate_service import ExchangeRateServiceInterface


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={"base_currency_code": "USD", "quote_currency_code": "EUR"},
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"

    data = response_json["data"]
    assert len(data) == 5

    assert data[0] == {
        "rate": "1.12",
        "date": "2024-04-02",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2024-01-01",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_start_date(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 3, 16)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "start_date": "2024-01-02",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"

    data = response_json["data"]
    assert len(data) == 3

    assert data[0] == {
        "rate": "1.05",
        "date": "2024-01-05",
    }
    assert data[-1] == {
        "rate": "1.02",
        "date": "2024-01-02",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_end_date(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 3, 16)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "end_date": "2024-01-05",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"

    data = response_json["data"]
    assert len(data) == 4

    assert data[0] == {
        "rate": "1.05",
        "date": "2024-01-05",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2024-01-01",
    }


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_with_start_and_end_date(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "start_date": "2023-12-31",
            "end_date": "2024-10-11",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"

    data = response_json["data"]
    assert len(data) == 6

    assert data[0] == {
        "rate": "0.98",
        "date": "2024-10-10",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2024-01-01",
    }


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_with_start_date_after_end_date(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "start_date": "2024-12-31",
            "end_date": "2023-03-15",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start_date must be before or equal to end_date",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_limit(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "limit": 2,
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"

    data = response_json["data"]
    assert len(data) == 2

    assert data[0] == {
        "rate": "1.02",
        "date": "2024-01-02",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2024-01-01",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_order_asc(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "order": "asc",
        },
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"

    data = response_json["data"]
    assert len(data) == 5

    assert data[0] == {
        "rate": "1",
        "date": "2024-01-01",
    }
    assert data[-1] == {
        "rate": "1.12",
        "date": "2024-04-02",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_start_date_after_today(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "start_date": "2024-04-02",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start_date must be before or equal to today; start_date must be before or equal to end_date",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_end_date_after_today(
    mock_date,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "end_date": "2030-04-01",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "end_date must be before or equal to today",
    }


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_invalid_base_currency(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={"base_currency_code": "XYZ", "quote_currency_code": "USD"},
    )
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Value error, Invalid currency code: XYZ"


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_invalid_quote_currency(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={"base_currency_code": "USD", "quote_currency_code": "XYZ"},
    )
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Value error, Invalid currency code: XYZ"
