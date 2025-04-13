import re
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ExchangeRateResponse(BaseModel):
    rate: Decimal = Field(gt=0)
    date: date
    from_iso_code: str
    to_iso_code: str

    @field_validator("from_iso_code", "to_iso_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{3}$", v):
            raise ValueError("Currency code must be 3 uppercase letters")
        return v
