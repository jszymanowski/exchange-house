import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_api_v1_currency_pairs(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get("/api/v1/currency_pairs")
    assert response.status_code == 200
    assert response.json() == [
        {
            "from_iso_code": "USD",
            "to_iso_code": "EUR",
        },
        {
            "from_iso_code": "EUR",
            "to_iso_code": "USD",
        },
        {
            "from_iso_code": "USD",
            "to_iso_code": "GBP",
        },
        {
            "from_iso_code": "GBP",
            "to_iso_code": "USD",
        },
    ]
