from datetime import date
from typing import Annotated, cast

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.dependencies import exchange_rate_service_dependency
from app.models import AvailableDate, Currency
from app.schema.exchange_rate_response import ExchangeRateResponse
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


def get_default_desired_date() -> AvailableDate:
    return cast(AvailableDate, date.today())


class LatestExchangeRateQueryParams(BaseModel):
    desired_date: AvailableDate = Field(default_factory=get_default_desired_date)


@router.get("/{base_currency_code}/{quote_currency_code}/latest")
async def latest_exchange_rate(
    base_currency_code: Currency,
    quote_currency_code: Currency,
    query_params: Annotated[LatestExchangeRateQueryParams, Query()],
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> ExchangeRateResponse:
    desired_date = query_params.desired_date

    validation_errors = []

    if base_currency_code != Currency("USD") and quote_currency_code != Currency("USD"):
        validation_errors.append("At least one currency must be USD")

    if validation_errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="; ".join(validation_errors),
        )

    result = await exchange_rate_service.get_latest_rate(base_currency_code, quote_currency_code, desired_date)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No exchange rate found for {base_currency_code} to {quote_currency_code} on {desired_date}",
        )

    return ExchangeRateResponse.from_model(result)
