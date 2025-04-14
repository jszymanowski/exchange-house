from datetime import date
from typing import Any, cast

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings

app = FastAPI()


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
    def __init__(self) -> None:
        self.base_url = "https://openexchangerates.org/api"
        self.headers = {"Content-Type": "application/json"}
        self.api_key = str(settings.OPEN_EXCHANGE_RATES_APP_ID)

        if not self.api_key:
            raise ValueError("OPEN_EXCHANGE_RATES_APP_ID is not set")

    async def historical_rates_for(self, date: date) -> HistoricalRatesResponse:
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


def get_open_exchange_rates_api_client() -> OpenExchangeRatesClient:
    return OpenExchangeRatesClient()
