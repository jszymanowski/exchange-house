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
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
        },
        {
            "base_currency_code": "EUR",
            "quote_currency_code": "USD",
        },
        {
            "base_currency_code": "USD",
            "quote_currency_code": "GBP",
        },
        {
            "base_currency_code": "GBP",
            "quote_currency_code": "USD",
        },
    ]
