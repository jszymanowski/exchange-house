from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from httpx import AsyncClient

from app.schema.exchange_rate_response import ExchangeRateResponse
from app.services.exchange_rate_service import ExchangeRateServiceInterface


@pytest.mark.asyncio
@patch("app.api.latest_exchange_rate.date")
async def test_api_v1_latest_exchange_rate(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"base_currency_code": "USD", "quote_currency_code": "EUR"},
    )
    assert response.status_code == 200

    response_data = response.json()
    assert ExchangeRateResponse(**response_data)
    assert response_data == {
        "rate": "1.02",
        "date": "2025-04-01",
        "base_currency_code": "USD",
        "quote_currency_code": "EUR",
    }


@pytest.mark.asyncio
@patch("app.api.latest_exchange_rate.date")
async def test_api_v1_latest_exchange_rate_with_desired_date(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
            "desired_date": "2024-01-02",
        },
    )
    assert response.status_code == 200

    response_data = response.json()
    assert ExchangeRateResponse(**response_data)
    assert response_data == {
        "rate": "1.02",
        "date": "2024-01-02",
        "base_currency_code": "USD",
        "quote_currency_code": "EUR",
    }


@pytest.mark.asyncio
async def test_api_v1_latest_exchange_rate_invalid_base_currency(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"base_currency_code": "XYZ", "quote_currency_code": "USD"},
    )
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert (
        response_detail[0]["msg"]
        == "Invalid currency code. See https://en.wikipedia.org/wiki/ISO_4217 . Bonds, testing "
        "and precious metals codes are not allowed."
    )


@pytest.mark.asyncio
async def test_api_v1_latest_exchange_rate_invalid_quote_currency(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"base_currency_code": "USD", "quote_currency_code": "XYZ"},
    )
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert (
        response_detail[0]["msg"] == "Invalid currency code. See https://en.wikipedia.org/wiki/ISO_4217 . Bonds, "
        "testing and precious metals codes are not allowed."
    )
