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


DEFAULT_PAGE = 1
DEFAULT_SIZE = 1_000
MAX_RECORDS_PER_REQUEST = DEFAULT_SIZE


class HistoricalExchangeRatesQueryParams(BaseModel):
    start_date: AvailableDate = Field(default_factory=get_default_start_date)
    end_date: AvailableDate = Field(default_factory=get_default_end_date)
    page: int = Field(default=DEFAULT_PAGE, ge=1)
    size: int = Field(default=DEFAULT_SIZE, ge=1, le=MAX_RECORDS_PER_REQUEST)
    order: Literal["asc", "desc"] = Field(default="desc")


@router.get("/{base_currency_code}/{quote_currency_code}/historical")
async def historical_exchange_rates(
    base_currency_code: Currency,
    quote_currency_code: Currency,
    query_params: Annotated[HistoricalExchangeRatesQueryParams, Query()],
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> HistoricalExchangeRateResponse:
    start_date = query_params.start_date
    end_date = query_params.end_date
    size = query_params.size
    page = query_params.page
    order = query_params.order

    offset = (page - 1) * size

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

    exchange_rates, total = await exchange_rate_service.get_historical_rates(
        base_currency_code=base_currency_code,
        quote_currency_code=quote_currency_code,
        start_date=start_date,
        end_date=end_date,
        limit=size,
        offset=offset,
        sort_order=order,
    )

    exchange_rate_data = [ExchangeRateData.from_model(exchange_rate) for exchange_rate in exchange_rates]

    return HistoricalExchangeRateResponse(
        base_currency_code=base_currency_code,
        quote_currency_code=quote_currency_code,
        data=exchange_rate_data,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )
