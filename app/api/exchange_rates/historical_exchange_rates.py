from datetime import date, timedelta
from typing import Annotated, Literal, cast

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.dependencies import exchange_rate_service_dependency
from app.models import AvailableDate, Currency
from app.schema.exchange_rate_response import (
    ExchangeRateData,
    HistoricalExchangeRateResponse,
)
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


def get_default_start_date() -> AvailableDate:
    return cast(AvailableDate, date.today() - timedelta(days=365.25 * 10))


def get_default_end_date() -> AvailableDate:
    return cast(AvailableDate, date.today())


MAX_RECORDS_PER_REQUEST = 10_000  # TODO: lower this with pagination
DEFAULT_LIMIT = 1_000


class HistoricalExchangeRatesQueryParams(BaseModel):
    start_date: AvailableDate = Field(default_factory=get_default_start_date)
    end_date: AvailableDate = Field(default_factory=get_default_end_date)
    limit: int = Field(default=DEFAULT_LIMIT, ge=1, le=MAX_RECORDS_PER_REQUEST)
    order: Literal["asc", "desc"] = Field(default="desc")


# TODO: Add pagination
@router.get("/{base_currency_code}/{quote_currency_code}/historical")
async def historical_exchange_rates(
    base_currency_code: Currency,
    quote_currency_code: Currency,
    query_params: Annotated[HistoricalExchangeRatesQueryParams, Query()],
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> HistoricalExchangeRateResponse:
    start_date = query_params.start_date
    end_date = query_params.end_date
    limit = query_params.limit
    order = query_params.order

    today = date.today()
    validation_errors = []

    if base_currency_code != Currency("USD") and quote_currency_code != Currency("USD"):
        validation_errors.append("At least one currency must be USD")

    if start_date > today:
        validation_errors.append("start_date must be before or equal to today")

    if end_date > today:
        validation_errors.append("end_date must be before or equal to today")

    if start_date > end_date:
        validation_errors.append("start_date must be before or equal to end_date")

    if validation_errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="; ".join(validation_errors),
        )

    exchange_rates = await exchange_rate_service.get_historical_rates(
        base_currency_code=base_currency_code,
        quote_currency_code=quote_currency_code,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        sort_order=order,
    )

    exchange_rate_data = [ExchangeRateData.from_model(exchange_rate) for exchange_rate in exchange_rates]

    return HistoricalExchangeRateResponse(
        base_currency_code=base_currency_code,
        quote_currency_code=quote_currency_code,
        data=exchange_rate_data,
    )
