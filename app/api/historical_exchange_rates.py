from datetime import date, timedelta
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.schema.exchange_rate_response import ExchangeRateResponse

router = APIRouter()


def get_default_start_date() -> date:
    return date.today() - timedelta(days=365.25 * 10)


def get_default_end_date() -> date:
    return date.today()


class HistoricalQueryParams(BaseModel):
    from_iso_code: str
    to_iso_code: str
    start_date: date = Field(default_factory=get_default_start_date)
    end_date: date = Field(default_factory=get_default_end_date)


@router.get("/historical_exchange_rates")
async def historical_exchange_rates(
    query_params: Annotated[HistoricalQueryParams, Query()],
) -> list[ExchangeRateResponse]:
    start_date = query_params.start_date
    end_date = query_params.end_date
    from_iso_code = query_params.from_iso_code
    to_iso_code = query_params.to_iso_code

    if start_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to today",
        )

    if end_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be before or equal to today",
        )

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before or equal to end_date",
        )

    return [
        ExchangeRateResponse(
            rate=Decimal(1.0),
            date=date,
            from_iso_code=from_iso_code,
            to_iso_code=to_iso_code,
        )
        for date in (
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        )
    ]
