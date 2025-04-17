import json
import re
from datetime import date
from importlib import resources

import httpx
import pytest
from pytest_httpx import HTTPXMock

from app.integrations.open_exchange_rates import (
    AuthenticationError,
    HistoricalRatesResponse,
    NotFoundError,
    OpenExchangeRatesClient,
    RequestError,
    RequestLimitError,
)


@pytest.fixture
def api_client() -> OpenExchangeRatesClient:
    return OpenExchangeRatesClient()


@pytest.mark.asyncio
class TestOpenExchangeRatesApi:
    async def test_historical_rates_for(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        fixture_data = json.loads(
            resources.files("tests.support.open_exchange_rates").joinpath("historical.json").read_text()
        )
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/historical/2023-01-02.json?app_id=FAKE_OER_APP_ID",
            json=fixture_data,
            status_code=200,
        )

        response = await api_client.historical_rates_for(date(2023, 1, 2))

        assert isinstance(response, HistoricalRatesResponse)
        assert response.base == "USD"
        assert isinstance(response.timestamp, int)

        assert response.rates["SGD"] == 1.3264
        assert response.rates["EUR"] == 0.913949
        assert response.rates["JPY"] == 142.17714286

        assert len(httpx_mock.get_requests()) == 1

    async def test_get_successful_response(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        response_data = {"success": "yay!"}
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            json=response_data,
            status_code=200,
        )

        response = await api_client.get("some_path")
        assert response == response_data
        assert len(httpx_mock.get_requests()) == 1

    async def test_get_400_error(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        error_response = {"error": True, "status": 400, "message": "not_available", "description": "That's not right."}
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            json=error_response,
            status_code=400,
        )

        with pytest.raises(RequestError, match="not_available: That's not right."):
            await api_client.get("some_path")
        assert len(httpx_mock.get_requests()) == 1

    async def test_get_401_error(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        error_response = {
            "error": True,
            "status": 401,
            "message": "invalid_app_id",
            "description": "Invalid App ID provided. Oopsie.",
        }
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            json=error_response,
            status_code=401,
        )

        with pytest.raises(AuthenticationError, match="Invalid App ID provided. Oopsie."):
            await api_client.get("some_path")
        assert len(httpx_mock.get_requests()) == 1

    async def test_get_403_error(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        error_response = {
            "error": True,
            "status": 403,
            "message": "missing_app_id",
            "description": "No App ID provided. Oopsie.",
        }
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            json=error_response,
            status_code=403,
        )

        with pytest.raises(AuthenticationError, match="No App ID provided. Oopsie."):
            await api_client.get("some_path")
        assert len(httpx_mock.get_requests()) == 1

    async def test_get_405_error(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            content=b"Method Not Allowed",
            status_code=405,
        )

        with pytest.raises(NotFoundError, match="/api/some_path not found: Method Not Allowed"):
            await api_client.get("some_path")
        assert len(httpx_mock.get_requests()) == 1

    async def test_get_429_error(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        error_response = {
            "error": True,
            "status": 429,
            "message": "too_many_requests",
            "description": "Access restricted until 2075-12-25 (reason: too_many_requests). If there has been a mistake, please contact support@openexchangerates.org.",
        }
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            json=error_response,
            status_code=429,
        )

        with pytest.raises(
            RequestLimitError,
            match=re.escape("Access restricted until 2075-12-25 (reason: too_many_requests)"),
        ):
            await api_client.get("some_path")
        assert len(httpx_mock.get_requests()) == 1

    async def test_get_unexpected_status_code(self, api_client: OpenExchangeRatesClient, httpx_mock: HTTPXMock) -> None:
        """Test that unexpected status codes are handled correctly."""
        httpx_mock.add_response(
            method="GET",
            url="https://openexchangerates.org/api/some_path?app_id=FAKE_OER_APP_ID",
            content=b"Internal Server Error",
            status_code=500,
        )

        with pytest.raises(httpx.HTTPStatusError):
            await api_client.get("some_path")
        assert len(httpx_mock.get_requests()) == 1
