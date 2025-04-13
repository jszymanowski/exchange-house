from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from app.data.valid_currencies import valid_currencies
from app.schema.exchange_rate_response import ExchangeRateResponse

router = APIRouter()


def get_default_desired_date() -> date:
    return date.today()


class LatestExchangeRateQueryParams(BaseModel):
    from_iso_code: str
    to_iso_code: str
    desired_date: date = Field(default_factory=get_default_desired_date)

    @field_validator("from_iso_code", "to_iso_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if v not in valid_currencies:
            raise ValueError(f"Invalid currency code: {v}")
        return v


@router.get("/latest_exchange_rate")
async def latest_exchange_rate(
    query_params: Annotated[LatestExchangeRateQueryParams, Query()],
) -> ExchangeRateResponse:
    from_iso_code = query_params.from_iso_code
    to_iso_code = query_params.to_iso_code
    desired_date = query_params.desired_date

    if from_iso_code not in valid_currencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid from_iso_code: {from_iso_code}",
        )

    if to_iso_code not in valid_currencies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid to_iso_code: {to_iso_code}",
        )

    return ExchangeRateResponse(
        rate=Decimal(1.0),
        date=desired_date,
        from_iso_code=from_iso_code,
        to_iso_code=to_iso_code,
    )
