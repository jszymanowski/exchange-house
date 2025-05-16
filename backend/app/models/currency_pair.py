from pydantic import BaseModel

from app.models.currency import Currency
from app.models.exchange_rate import ExchangeRate


class CurrencyPair(BaseModel):
    base_currency_code: Currency
    quote_currency_code: Currency

    @classmethod
    def from_db(cls, model: ExchangeRate) -> "CurrencyPair":
        return cls(
            base_currency_code=Currency(model.base_currency_code),
            quote_currency_code=Currency(model.quote_currency_code),
        )
