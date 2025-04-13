import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_v1_latest_exchange_rate(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        "/api/v1/latest_exchange_rate",
        params={"from_iso_code": "USD", "to_iso_code": "EUR"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "rate": "1",
        "date": "2025-04-01",
        "from_iso_code": "USD",
        "to_iso_code": "EUR",
    }
