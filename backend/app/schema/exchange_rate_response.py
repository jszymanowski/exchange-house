from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models import Currency, ExchangeRate


class ExchangeRateData(BaseModel):
    rate: Decimal = Field(gt=0)
    date: date

    @classmethod
    def from_model(cls, model: ExchangeRate) -> "ExchangeRateData":
        return cls(
            rate=model.rate,
            date=model.as_of,
        )


class ExchangeRateResponse(BaseModel):
    base_currency_code: Currency
    quote_currency_code: Currency
    data: ExchangeRateData

    @classmethod
    def from_model(cls, model: ExchangeRate) -> "ExchangeRateResponse":
        data = ExchangeRateData.from_model(model)
        return cls(
            base_currency_code=Currency(model.base_currency_code),
            quote_currency_code=Currency(model.quote_currency_code),
            data=data,
        )


class HistoricalExchangeRateResponse(BaseModel):
    base_currency_code: Currency
    quote_currency_code: Currency
    data: list[ExchangeRateData]
    total: int
    page: int
    size: int
    pages: int
