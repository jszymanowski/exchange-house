from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from httpx import AsyncClient, Response

from app.services.exchange_rate_service import ExchangeRateServiceInterface


def assert_historical_exchange_rates_response(
    response: Response,
    first_data: dict[str, str],
    last_data: dict[str, str],
    total: int = 8,
    data_size: int = 5,
    size: int = 1000,
    page: int = 1,
    pages: int = 1,
) -> None:
    response_json = response.json()
    assert response_json.keys() == {
        "base_currency_code",
        "quote_currency_code",
        "data",
        "total",
        "page",
        "size",
        "pages",
    }

    assert response_json["base_currency_code"] == "USD"
    assert response_json["quote_currency_code"] == "EUR"
    assert response_json["total"] == total
    assert response_json["size"] == size
    assert response_json["page"] == page
    assert response_json["pages"] == pages

    data = response_json["data"]
    assert len(data) == data_size

    assert data[0] == first_data
    assert data[-1] == last_data


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical")
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        first_data={
            "rate": "1.12",
            "date": "2024-04-02",
        },
        last_data={
            "rate": "1",
            "date": "2024-01-01",
        },
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_start_date(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 3, 16)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"start_date": "2024-01-02"})
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        data_size=3,
        first_data={
            "rate": "1.05",
            "date": "2024-01-05",
        },
        last_data={
            "rate": "1.02",
            "date": "2024-01-02",
        },
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_end_date(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 3, 16)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"end_date": "2024-01-05"})
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        data_size=4,
        first_data={
            "rate": "1.05",
            "date": "2024-01-05",
        },
        last_data={
            "rate": "1",
            "date": "2024-01-01",
        },
    )


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_with_start_and_end_date(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/exchange_rates/USD/EUR/historical",
        params={
            "start_date": "2023-12-31",
            "end_date": "2024-10-11",
        },
    )
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        data_size=6,
        first_data={
            "rate": "0.98",
            "date": "2024-10-10",
        },
        last_data={
            "rate": "1",
            "date": "2024-01-01",
        },
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_limit(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": 2})
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        size=2,
        data_size=2,
        first_data={
            "rate": "1.02",
            "date": "2024-01-02",
        },
        last_data={
            "rate": "1",
            "date": "2024-01-01",
        },
        pages=4,
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_offset_and_limit(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"page": 2, "size": 2})
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        size=2,
        data_size=2,
        first_data={
            "rate": "1.05",
            "date": "2024-01-05",
        },
        last_data={
            "rate": "1.04",
            "date": "2024-01-03",
        },
        page=2,
        pages=4,
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_order_asc(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"order": "asc"})
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        first_data={
            "rate": "1",
            "date": "2024-01-01",
        },
        last_data={
            "rate": "1.12",
            "date": "2024-04-02",
        },
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_order_desc(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical")
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        first_data={
            "rate": "1.12",
            "date": "2024-04-02",
        },
        last_data={
            "rate": "1",
            "date": "2024-01-01",
        },
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_limit_and_order_asc(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 5)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": 2, "order": "asc"})
    assert response.status_code == 200

    assert_historical_exchange_rates_response(
        response,
        data_size=2,
        first_data={
            "rate": "1",
            "date": "2024-01-01",
        },
        last_data={
            "rate": "1.02",
            "date": "2024-01-02",
        },
        size=2,
        pages=4,
    )


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_start_date_after_today(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"start_date": "2024-04-02"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": "start_date must be before or equal to today; start_date must be before or equal to end_date",
    }


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_without_usd(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/JPY/EUR/historical")
    assert response.status_code == 422
    assert response.json() == {"detail": "At least one currency must be USD"}


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_with_start_date_after_end_date(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get(
        "/api/v1/exchange_rates/USD/EUR/historical",
        params={
            "start_date": "2024-12-31",
            "end_date": "2023-03-15",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": "start_date must be before or equal to end_date",
    }


@pytest.mark.asyncio
@patch("app.api.exchange_rates.historical_exchange_rates.date")
async def test_api_v1_historical_exchange_rates_with_end_date_after_today(
    mock_date: MagicMock,
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    fixed_date = date(2024, 4, 1)
    mock_date.today.return_value = fixed_date

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"end_date": "2030-04-01"})
    assert response.status_code == 422
    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Date must be in the past or today"


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_invalid_base_currency(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/XYZ/USD/historical")
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert (
        response_detail[0]["msg"] == "Invalid currency code. See https://en.wikipedia.org/wiki/ISO_4217 . Bonds, "
        "testing and precious metals codes are not allowed."
    )


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_invalid_quote_currency(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/USD/XYZ/historical")
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert (
        response_detail[0]["msg"]
        == "Invalid currency code. See https://en.wikipedia.org/wiki/ISO_4217 . Bonds, testing "
        "and precious metals codes are not allowed."
    )


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_with_invalid_limit(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": "-1"})
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Input should be greater than or equal to 1"

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": "0"})
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Input should be greater than or equal to 1"

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": "999999999"})
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Input should be less than or equal to 1000"

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": "3.14159"})
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"size": "INFINITYANDBEYOND"})
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.asyncio
async def test_api_v1_historical_exchange_rates_with_invalid_order(
    async_client: AsyncClient,
    with_test_exchange_rate_service: ExchangeRateServiceInterface,
) -> None:
    response = await async_client.get("/api/v1/exchange_rates/USD/EUR/historical", params={"order": "random"})
    assert response.status_code == 422

    response_detail = response.json()["detail"]
    assert len(response_detail) == 1
    assert response_detail[0]["msg"] == "Input should be 'asc' or 'desc'"
