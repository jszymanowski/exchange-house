from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class SimpleRateResponse(BaseModel):
    rate: Decimal = Field(gt=0)
    date: date
