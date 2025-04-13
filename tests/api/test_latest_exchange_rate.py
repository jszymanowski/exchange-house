from datetime import date
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.schema.exchange_rate_response import ExchangeRateResponse


@pytest.mark.asyncio
@patch("app.api.latest_exchange_rate.date")
async def test_api_v1_latest_exchange_rate(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"from_iso_code": "USD", "to_iso_code": "EUR"},
    )
    assert response.status_code == 200

    response_data = response.json()
    assert ExchangeRateResponse(**response_data)
    assert response_data == {
        "rate": "1",
        "date": "2025-04-01",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }


@pytest.mark.asyncio
@patch("app.api.latest_exchange_rate.date")
async def test_api_v1_latest_exchange_rate_with_desired_date(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
            "desired_date": "2025-03-15",
        },
    )
    assert response.status_code == 200

    response_data = response.json()
    assert ExchangeRateResponse(**response_data)
    assert response_data == {
        "rate": "1",
        "date": "2025-03-15",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }


@pytest.mark.asyncio
async def test_api_v1_latest_exchange_rate_invalid_base_currency(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"from_iso_code": "XYZ", "to_iso_code": "USD"},
    )
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Value error, Invalid currency code: XYZ"


@pytest.mark.asyncio
async def test_api_v1_latest_exchange_rate_invalid_quote_currency(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"from_iso_code": "USD", "to_iso_code": "XYZ"},
    )
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Value error, Invalid currency code: XYZ"
