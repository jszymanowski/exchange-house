from pydantic import BaseModel

from app.models.exchange_rate import ExchangeRate


class CurrencyPair(BaseModel):
    base_currency_code: str
    quote_currency_code: str

    @classmethod
    def from_db(cls, model: ExchangeRate) -> "CurrencyPair":
        return cls(
            base_currency_code=model.base_currency_code,
            quote_currency_code=model.quote_currency_code,
        )
