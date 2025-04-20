from pydantic import BaseModel

from app.models import Currency


class CurrencyPairData(BaseModel):
    base_currency_code: Currency
    quote_currency_code: Currency


class CurrencyPairResponse(BaseModel):
    data: list[CurrencyPairData]
