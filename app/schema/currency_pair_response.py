from pydantic import BaseModel

from app.models import Currency


class CurrencyPairResponse(BaseModel):
    base_currency_code: Currency
    quote_currency_code: Currency
