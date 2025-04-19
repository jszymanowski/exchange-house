import pytest
from httpx import AsyncClient

from app.services.exchange_rate_service import ExchangeRateServiceInterface


@pytest.mark.asyncio
async def test_api_v1_available_dates(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/available_dates")
    assert response.status_code == 200
    assert response.json() == [
        "2025-04-01",
        "2025-04-02",
        "2025-04-03",
    ]
