from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Query

from app.schema.exchange_rate_response import ExchangeRateResponse

router = APIRouter(prefix="/api/v1")


@router.get("/latest_exchange_rate")
async def latest_exchange_rate(
    from_iso_code: str = Query(..., alias="from_iso_code"),
    to_iso_code: str = Query(..., alias="to_iso_code"),
) -> ExchangeRateResponse:
    return ExchangeRateResponse(
        rate=Decimal(1.0),
        date=date.today(),
        from_iso_code=from_iso_code,
        to_iso_code=to_iso_code,
    )
