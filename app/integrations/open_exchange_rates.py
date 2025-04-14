from datetime import date
from typing import Any, cast

import httpx
from pydantic import BaseModel

from app.core.config import settings


class OpenExchangeRatesError(Exception):
    pass


class AuthenticationError(OpenExchangeRatesError):
    pass


class RequestError(OpenExchangeRatesError):
    pass


class NotFoundError(OpenExchangeRatesError):
    pass


class HistoricalRatesResponse(BaseModel):
    disclaimer: str
    license: str
    timestamp: int
    base: str
    rates: dict[str, float]


class OpenExchangeRatesClient:
    def __init__(self, timeout: float = 30.0) -> None:
        """Initialize the Open Exchange Rates API client.

        Args:
            timeout: Request timeout in seconds.

        Raises:
            ValueError: If the API key is not set in the environment.
        """
        self.base_url = "https://openexchangerates.org/api"
        self.headers = {"Content-Type": "application/json"}
        self.timeout = timeout
        self.api_key = str(settings.open_exchange_rates_app_id)
        if not self.api_key:
            raise ValueError("OPEN_EXCHANGE_RATES_APP_ID is not set")

    async def historical_rates_for(self, date: date) -> HistoricalRatesResponse:
        """Fetch historical exchange rates for a specific date.

        Args:
            date: The date to fetch rates for.

        Returns:
            HistoricalRatesResponse: The parsed response with exchange rates.

        Raises:
            AuthenticationError: If authentication fails.
            RequestError: If the request is invalid.
            NotFoundError: If the resource is not found.
        """
        response = await self.get(f"historical/{date.strftime('%Y-%m-%d')}.json")
        return HistoricalRatesResponse.model_validate(response)

    async def get(self, path: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            request_url = f"{self.base_url}/{path}"
            params = {"app_id": self.api_key}
            response = await client.get(request_url, headers=self.headers, params=params)

            if response.status_code == 403:
                error_data = response.json()
                raise AuthenticationError(error_data["description"])
            elif response.status_code == 400:
                error_data = response.json()
                raise RequestError(f"{error_data['message']}: {error_data['description']}")
            elif response.status_code in (404, 405):
                raise NotFoundError(f"/api/{path} not found: {response.text}")

            response.raise_for_status()
            return cast(dict[str, Any], response.json())
