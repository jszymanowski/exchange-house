from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models import Currency, ExchangeRate


class ExchangeRateResponse(BaseModel):
    rate: Decimal = Field(gt=0)
    date: date
    base_currency_code: Currency
    quote_currency_code: Currency

    @classmethod
    def from_model(cls, model: ExchangeRate) -> "ExchangeRateResponse":
        return cls(
            rate=model.rate,
            date=model.as_of,
            base_currency_code=Currency(model.base_currency_code),
            quote_currency_code=Currency(model.quote_currency_code),
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
    base_currency_code: Currency
    quote_currency_code: Currency
    data: list[ExchangeRateData]
