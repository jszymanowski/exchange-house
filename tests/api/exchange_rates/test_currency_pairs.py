import pytest
from httpx import AsyncClient

from app.services.exchange_rate_service import ExchangeRateServiceInterface


@pytest.mark.asyncio
async def test_api_v1_currency_pairs(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/available_currency_pairs")
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 8
    assert response_data == [
        {
            "base_currency_code": "EUR",
            "quote_currency_code": "USD",
        },
        {
            "base_currency_code": "GBP",
            "quote_currency_code": "USD",
        },
        {
            "base_currency_code": "JPY",
            "quote_currency_code": "USD",
        },
        {
            "base_currency_code": "SGD",
            "quote_currency_code": "USD",
        },
        {
            "base_currency_code": "USD",
            "quote_currency_code": "EUR",
        },
        {
            "base_currency_code": "USD",
            "quote_currency_code": "GBP",
        },
        {
            "base_currency_code": "USD",
            "quote_currency_code": "JPY",
        },
        {
            "base_currency_code": "USD",
            "quote_currency_code": "SGD",
        },
    ]
