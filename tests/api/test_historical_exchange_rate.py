from datetime import date
from unittest.mock import patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@patch("app.api.main.date")
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
