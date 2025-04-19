import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TypedDict, Unpack

from app.models import Currency, ExchangeRate


class ExchangeRateParams(TypedDict, total=False):
    id: uuid.UUID
    as_of: date
    base_currency_code: Currency
    quote_currency_code: Currency
    rate: Decimal
    data_source: str
    created_at: datetime | None
    updated_at: datetime | None


def build_exchange_rate(**kwargs: Unpack[ExchangeRateParams]) -> ExchangeRate:
    defaults: ExchangeRateParams = {
        "as_of": date.today(),
        "base_currency_code": Currency("USD"),
        "quote_currency_code": Currency("EUR"),
        "rate": Decimal("0.85000000"),
        "data_source": "test",
    }
    attributes = defaults | kwargs

    return ExchangeRate(**attributes)


def build_exchange_rate_pair(**kwargs: Unpack[ExchangeRateParams]) -> tuple[ExchangeRate, ExchangeRate]:
    defaults: ExchangeRateParams = {
        "as_of": date.today(),
        "base_currency_code": Currency("USD"),
        "quote_currency_code": Currency("EUR"),
        "rate": Decimal("0.85000000"),
        "data_source": "test",
    }
    attributes = defaults | kwargs
    inverse_attributes: ExchangeRateParams = attributes | {
        "base_currency_code": attributes["quote_currency_code"],
        "quote_currency_code": attributes["base_currency_code"],
        "rate": Decimal("1.00000000") / attributes["rate"],
    }

    return build_exchange_rate(**attributes), build_exchange_rate(**inverse_attributes)
