from datetime import date
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.dependencies import exchange_rate_service_dependency
from app.models import AvailableDate, Currency
from app.schema.exchange_rate_response import ExchangeRateResponse
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


def get_default_desired_date() -> date:
    return date.today()


class LatestExchangeRateQueryParams(BaseModel):
    base_currency_code: Currency
    quote_currency_code: Currency
    desired_date: AvailableDate | None = Field(default_factory=get_default_desired_date)


@router.get("/latest_exchange_rate")
async def latest_exchange_rate(
    query_params: Annotated[LatestExchangeRateQueryParams, Query()],
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> ExchangeRateResponse:
    base_currency_code = query_params.base_currency_code
    quote_currency_code = query_params.quote_currency_code
    desired_date = query_params.desired_date or date.today()

    result = await exchange_rate_service.get_latest_rate(base_currency_code, quote_currency_code, desired_date)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No exchange rate found for {base_currency_code} to {quote_currency_code} on {desired_date}",
        )

    return ExchangeRateResponse.from_model(result)
