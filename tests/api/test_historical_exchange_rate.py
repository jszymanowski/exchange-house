from datetime import date
from unittest.mock import patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rate(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={"from_iso_code": "USD", "to_iso_code": "EUR"},
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3653

    assert data[0] == {
        "rate": "1",
        "date": "2015-04-02",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2025-04-01",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rate_with_start_date(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
            "start_date": "2024-12-31",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 92

    assert data[0] == {
        "rate": "1",
        "date": "2024-12-31",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2025-04-01",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rate_with_end_date(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
            "end_date": "2024-12-31",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3562

    assert data[0] == {
        "rate": "1",
        "date": "2015-04-02",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2024-12-31",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rate_with_start_and_end_date(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
            "start_date": "2024-12-31",
            "end_date": "2025-03-15",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 75

    assert data[0] == {
        "rate": "1",
        "date": "2024-12-31",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }
    assert data[-1] == {
        "rate": "1",
        "date": "2025-03-15",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rate_with_start_date_after_end_date(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
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
async def test_api_v1_historical_exchange_rate_with_start_date_after_today(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
            "start_date": "2025-04-02",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start_date must be before or equal to today",
    }


@pytest.mark.asyncio
@patch("app.api.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rate_with_end_date_after_today(
    mock_date,
    async_client: AsyncClient,
) -> None:
    fixed_date = date(2025, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get(
        "/api/v1/historical_exchange_rates",
        params={
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
            "end_date": "2030-04-01",
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "end_date must be before or equal to today",
    }
