from datetime import date, timedelta
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from app.data.valid_currencies import valid_currencies
from app.schema.exchange_rate_response import ExchangeRateResponse

router = APIRouter()


def get_default_start_date() -> date:
    return date.today() - timedelta(days=365.25 * 10)


def get_default_end_date() -> date:
    return date.today()


class HistoricalExchangeRatesQueryParams(BaseModel):
    base_currency_code: str
    quote_currency_code: str
    start_date: date = Field(default_factory=get_default_start_date)
    end_date: date = Field(default_factory=get_default_end_date)

    @field_validator("base_currency_code", "quote_currency_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if v not in valid_currencies:
            raise ValueError(f"Invalid currency code: {v}")
        return v


# TODO: Add pagination
@router.get("/historical_exchange_rates")
async def historical_exchange_rates(
    query_params: Annotated[HistoricalExchangeRatesQueryParams, Query()],
) -> list[ExchangeRateResponse]:
    start_date = query_params.start_date
    end_date = query_params.end_date
    base_currency_code = query_params.base_currency_code
    quote_currency_code = query_params.quote_currency_code

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

    return [
        ExchangeRateResponse(
            rate=Decimal(1.0),
            date=date,
            base_currency_code=base_currency_code,
            quote_currency_code=quote_currency_code,
        )
        for date in (start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1))
    ]
