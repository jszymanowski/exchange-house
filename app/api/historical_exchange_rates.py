from datetime import date, timedelta
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from app.core.dependencies import exchange_rate_service_dependency
from app.data.currencies import is_valid_currency
from app.schema.exchange_rate_response import (
    ExchangeRateData,
    HistoricalExchangeRateResponse,
)
from app.services.exchange_rate_service import ExchangeRateServiceInterface

router = APIRouter()


def get_default_start_date() -> date:
    return date.today() - timedelta(days=365.25 * 10)


def get_default_end_date() -> date:
    return date.today()


MAX_RECORDS_PER_REQUEST = 1_000


class HistoricalExchangeRatesQueryParams(BaseModel):
    base_currency_code: str
    quote_currency_code: str
    start_date: date = Field(default_factory=get_default_start_date)
    end_date: date = Field(default_factory=get_default_end_date)
    limit: int = Field(default=MAX_RECORDS_PER_REQUEST, ge=1, le=MAX_RECORDS_PER_REQUEST)
    order: Literal["asc", "desc"] = Field(default="desc")

    @field_validator("base_currency_code", "quote_currency_code")
    @classmethod
    def validate_iso_code(cls, value: str) -> str:
        if not is_valid_currency(value):
            raise ValueError(f"Invalid currency code: {value}")
        return value


# TODO: Add pagination
@router.get("/historical_exchange_rates")
async def historical_exchange_rates(
    query_params: Annotated[HistoricalExchangeRatesQueryParams, Query()],
    exchange_rate_service: ExchangeRateServiceInterface = exchange_rate_service_dependency,
) -> HistoricalExchangeRateResponse:
    start_date = query_params.start_date
    end_date = query_params.end_date
    base_currency_code = query_params.base_currency_code
    quote_currency_code = query_params.quote_currency_code
    limit = query_params.limit
    order = query_params.order

    today = date.today()
    validation_errors = []

    if start_date > today:
        validation_errors.append("start_date must be before or equal to today")

    if end_date > today:
        validation_errors.append("end_date must be before or equal to today")

    if start_date > end_date:
        validation_errors.append("start_date must be before or equal to end_date")

    if validation_errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
