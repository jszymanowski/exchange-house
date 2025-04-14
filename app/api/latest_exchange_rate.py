from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from app.core.dependencies import exchange_rate_service_dependency
from app.data.valid_currencies import valid_currencies
from app.schema.exchange_rate_response import ExchangeRateResponse
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


def get_default_desired_date() -> date:
    return date.today()


class LatestExchangeRateQueryParams(BaseModel):
    base_currency_code: str
    quote_currency_code: str
    desired_date: date | None = Field(default_factory=get_default_desired_date)

    @field_validator("base_currency_code", "quote_currency_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if v not in valid_currencies:
            raise ValueError(f"Invalid currency code: {v}")
        return v


@router.get("/latest_exchange_rate")
async def latest_exchange_rate(
    query_params: Annotated[LatestExchangeRateQueryParams, Query()],
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> ExchangeRateResponse:
    base_currency_code = query_params.base_currency_code
    quote_currency_code = query_params.quote_currency_code
    desired_date = query_params.desired_date or date.today()

    if base_currency_code not in valid_currencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid base_currency_code: {base_currency_code}",
        )

    if quote_currency_code not in valid_currencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid quote_currency_code: {quote_currency_code}",
        )

    result = await exchange_rate_service.get_latest_rate(base_currency_code, quote_currency_code, desired_date)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No exchange rate found for {base_currency_code} to {quote_currency_code} on {desired_date}",
        )

    return ExchangeRateResponse.from_model(result)
