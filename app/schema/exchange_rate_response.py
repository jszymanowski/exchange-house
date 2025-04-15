import re
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.models.exchange_rate import ExchangeRate


class ExchangeRateResponse(BaseModel):
    rate: Decimal = Field(gt=0)
    date: date
    base_currency_code: str
    quote_currency_code: str

    @field_validator("base_currency_code", "quote_currency_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{3}$", v):
            raise ValueError("Currency code must be 3 uppercase letters")
        return v

    @classmethod
    def from_model(cls, model: ExchangeRate) -> "ExchangeRateResponse":
        return cls(
            rate=model.rate,
            date=model.as_of,
            base_currency_code=model.base_currency_code,
            quote_currency_code=model.quote_currency_code,
        )


class ExchangeRateData(BaseModel):
    rate: Decimal = Field(gt=0)
    date: date

    @classmethod
    def from_model(cls, model: ExchangeRate) -> "ExchangeRateData":
        return cls(
            rate=model.rate,
            date=model.as_of,
        )


class HistoricalExchangeRateResponse(BaseModel):
    base_currency_code: str
    quote_currency_code: str
    data: list[ExchangeRateData]

    @field_validator("base_currency_code", "quote_currency_code")
    @classmethod
    def validate_iso_code(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{3}$", v):
            raise ValueError("Currency code must be 3 uppercase letters")
        return v
