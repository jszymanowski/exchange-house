from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class ExchangeRateResponse(BaseModel):
    rate: Decimal
    date: date
    from_iso_code: str
    to_iso_code: str
